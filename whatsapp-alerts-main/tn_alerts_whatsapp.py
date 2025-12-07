#!/usr/bin/env python3
"""
tn_alerts_whatsapp.py

Usage:
  - Edit environment variables (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM)
  - Optionally set RECIPIENT_WHATSAPP (= 'whatsapp:+91XXXXXXXXXX')
  - Run: python tn_alerts_whatsapp.py
"""

import os
import pandas as pd
from datetime import datetime, date, timedelta
from twilio.rest import Client
import math
from dotenv import load_dotenv
load_dotenv()


# ----- Configuration -----
VACC_CSV = r"C:\project_root\twilio\vaccinations_india.csv"
OUTBREAK_CSV = r"C:\project_root\twilio\outbreaks_india.csv"


# Dummy user/location sample. Replace "Tamil Nadu" or add district for more precision.
USER_STATE = "Tamil Nadu"
USER_DISTRICT = None  # e.g., "Chennai" or None to monitor whole state

# Alert thresholds/settings
OUTBREAK_DAYS_WINDOW = 14
VACC_UPCOMING_DAYS = 30
OUTBREAK_CASES_THRESHOLD = 50   # consider outbreak noteworthy if cases_reported >= this
MAX_ALERT_ITEMS = 5             # limit details in a single message

# Twilio config from environment

TWILIO_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.environ.get("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")  # sandbox default
RECIPIENT_WHATSAPP = os.environ.get("RECIPIENT_WHATSAPP", "whatsapp:+917343246348")

# Test mode: if True, messages are printed instead of sent to Twilio
DRY_RUN = False


# ----- Utilities -----
def safe_to_datetime(x):
    """Robust parse of date-like strings to datetime.date (fallback None)."""
    try:
        if pd.isna(x) or x == "":
            return None
        x = str(x).strip()
        # pandas to_datetime can handle many formats
        ts = pd.to_datetime(x, dayfirst=False, errors="coerce")
        if pd.isna(ts):
            # try day-first parse
            ts = pd.to_datetime(x, dayfirst=True, errors="coerce")
        if pd.isna(ts):
            return None
        return ts.date()
    except Exception:
        return None

def load_and_normalize_vaccines(path):
    df = pd.read_csv(path, dtype=str)
    df.columns = [c.strip() for c in df.columns]
    # Ensure important columns exist
    expected = ["campaign_id","country","state","district","start_date","end_date","vaccine_name","target_population","doses_allocated","doses_administered","partner_org","notes"]
    # fill missing expected columns
    for c in expected:
        if c not in df.columns:
            df[c] = ""
    # Normalize case and whitespace
    df['state'] = df['state'].astype(str).str.strip().str.title()
    df['district'] = df['district'].astype(str).str.strip().str.title()
    # Parse dates
    df['start_date_parsed'] = df['start_date'].apply(safe_to_datetime)
    df['end_date_parsed'] = df['end_date'].apply(safe_to_datetime)
    # Numeric fields
    for col in ['doses_allocated','doses_administered']:
        df[col + "_num"] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    return df

def load_and_normalize_outbreaks(path):
    df = pd.read_csv(path, dtype=str)
    df.columns = [c.strip() for c in df.columns]
    expected = ["outbreak_id","disease","report_date","country","state","district","cases_reported","deaths","severity","confirmed","source_url","notes"]
    for c in expected:
        if c not in df.columns:
            df[c] = ""
    df['state'] = df['state'].astype(str).str.strip().str.title()
    df['district'] = df['district'].astype(str).str.strip().str.title()
    df['report_date_parsed'] = df['report_date'].apply(safe_to_datetime)
    df['cases_reported_num'] = pd.to_numeric(df['cases_reported'], errors='coerce').fillna(0).astype(int)
    df['deaths_num'] = pd.to_numeric(df['deaths'], errors='coerce').fillna(0).astype(int)
    df['severity'] = df['severity'].astype(str).str.strip().str.lower()
    return df

# ----- Alert builders -----
def build_vaccine_alerts(vac_df, user_state, user_district=None):
    today = date.today()
    # filter by state/district
    df = vac_df[vac_df['state'].str.lower() == user_state.strip().lower()]
    if user_district:
        df = df[df['district'].str.lower() == user_district.strip().lower()]
    # ongoing: start_date_parsed <= today <= end_date_parsed
    ongoing = df[(df['start_date_parsed'].notnull()) & (df['end_date_parsed'].notnull()) & 
                 (df['start_date_parsed'] <= today) & (df['end_date_parsed'] >= today)]
    # upcoming: start_date within next VACC_UPCOMING_DAYS
    upcoming_cut = today + timedelta(days=VACC_UPCOMING_DAYS)
    upcoming = df[(df['start_date_parsed'].notnull()) & 
                  (df['start_date_parsed'] > today) & (df['start_date_parsed'] <= upcoming_cut)]
    # sort for stable output
    ongoing = ongoing.sort_values(by='start_date_parsed', ascending=True)
    upcoming = upcoming.sort_values(by='start_date_parsed', ascending=True)
    return ongoing, upcoming

def build_outbreak_alerts(out_df, user_state, user_district=None):
    today = date.today()
    since = today - timedelta(days=OUTBREAK_DAYS_WINDOW)
    df = out_df[out_df['state'].str.lower() == user_state.strip().lower()]
    if user_district:
        df = df[df['district'].str.lower() == user_district.strip().lower()]
    # recent
    recent = df[df['report_date_parsed'].notnull() & (df['report_date_parsed'] >= since)]
    # prioritize serious ones
    serious = recent[(recent['severity'].isin(['high','moderate'])) | (recent['cases_reported_num'] >= OUTBREAK_CASES_THRESHOLD)]
    other = recent[~recent.index.isin(serious.index)]
    serious = serious.sort_values(by=['report_date_parsed','cases_reported_num'], ascending=[False, False])
    other = other.sort_values(by=['report_date_parsed','cases_reported_num'], ascending=[False, False])
    return serious, other

# ----- Message composition & sending -----
def compose_message(ongoing_vac, upcoming_vac, serious_out, other_out, user_state, user_district=None):
    parts = []
    header = f"Health Alerts for {user_state}"
    if user_district:
        header += f", {user_district}"
    header += f" — {date.today().isoformat()}"
    parts.append(header)
    parts.append("")  # blank line

    # Vaccines
    if len(ongoing_vac) + len(upcoming_vac) == 0:
        parts.append("Vaccination updates: No ongoing or upcoming campaigns in the next {} days.".format(VACC_UPCOMING_DAYS))
    else:
        parts.append("Vaccination updates:")
        # show ongoing first
        shown = 0
        for _, r in ongoing_vac.head(MAX_ALERT_ITEMS).iterrows():
            parts.append(f"- ONGOING: {r['vaccine_name']} for {r['target_population']} in {r['district']}. ({r['start_date_parsed']} → {r['end_date_parsed']}), doses administered: {r['doses_administered_num']}")
            shown += 1
        for _, r in upcoming_vac.head(max(0, MAX_ALERT_ITEMS - shown)).iterrows():
            parts.append(f"- UPCOMING: {r['vaccine_name']} for {r['target_population']} in {r['district']}. Starts: {r['start_date_parsed']}. Allocated: {r['doses_allocated']}")
        if (len(ongoing_vac) + len(upcoming_vac)) > MAX_ALERT_ITEMS:
            parts.append(f"...and {len(ongoing_vac)+len(upcoming_vac)-MAX_ALERT_ITEMS} more vaccination events.")

    parts.append("")  # blank

    # Outbreaks
    total_recent = len(serious_out) + len(other_out)
    if total_recent == 0:
        parts.append(f"No outbreaks reported in the last {OUTBREAK_DAYS_WINDOW} days.")
    else:
        parts.append(f"Outbreak reports (last {OUTBREAK_DAYS_WINDOW} days): {total_recent} (priority shown first)")
        shown = 0
        for _, r in serious_out.head(MAX_ALERT_ITEMS).iterrows():
            parts.append(f"- {r['disease']} ({r['severity'].upper()}): {r['cases_reported_num']} cases in {r['district']} on {r['report_date_parsed']}. Confirmed: {r['confirmed']}.")
            shown += 1
        for _, r in other_out.head(max(0, MAX_ALERT_ITEMS - shown)).iterrows():
            parts.append(f"- {r['disease']} ({r['severity']}): {r['cases_reported_num']} cases in {r['district']} on {r['report_date_parsed']}.")
        if total_recent > MAX_ALERT_ITEMS:
            parts.append(f"...and {total_recent - MAX_ALERT_ITEMS} more recent reports.")
    parts.append("")  # blank

    parts.append("Note: This dataset is synthetic/demo. Replace with real feed for production.")
    return "\n".join(parts)

def send_whatsapp_message(body, recipient=RECIPIENT_WHATSAPP, dry_run=DRY_RUN):
    print("---- MESSAGE PREVIEW ----")
    print(body)
    print("---- END PREVIEW ----")
    if dry_run:
        print("[DRY RUN] Not sending message to Twilio.")
        return {"status": "dry_run", "sid": None}
    if not (TWILIO_SID and TWILIO_TOKEN and TWILIO_WHATSAPP_FROM and recipient):
        raise RuntimeError("Missing Twilio configuration. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_WHATSAPP_FROM.")
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=recipient,
        body=body
    )
    print("Sent message SID:", message.sid)
    return {"status": "sent", "sid": message.sid}

# ----- Main flow -----
def main():
    print("Loading datasets...")
    vac_df = load_and_normalize_vaccines(VACC_CSV)
    out_df = load_and_normalize_outbreaks(OUTBREAK_CSV)
    print("Datasets loaded. Building alerts for:", USER_STATE, USER_DISTRICT)

    ongoing_vac, upcoming_vac = build_vaccine_alerts(vac_df, USER_STATE, USER_DISTRICT)
    serious_out, other_out = build_outbreak_alerts(out_df, USER_STATE, USER_DISTRICT)

    msg = compose_message(ongoing_vac, upcoming_vac, serious_out, other_out, USER_STATE, USER_DISTRICT)
    result = send_whatsapp_message(msg)
    print("Result:", result)

if __name__ == "__main__":
    main()
