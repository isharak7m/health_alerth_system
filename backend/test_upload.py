import requests
import io

# Test CSV content
csv_content = """outbreak_id,disease,report_date,state,district,cases_reported,deaths,severity,confirmed,country,source_url,notes
OUT003,Malaria,2024-01-15,Delhi,New Delhi,25,1,moderate,true,India,,Monsoon related"""

# Create a file-like object
csv_file = io.StringIO(csv_content)

# Test the upload
files = {'file': ('test.csv', csv_content, 'text/csv')}

try:
    response = requests.post(
        'http://localhost:8002/api/admin/outbreaks/upload-csv',
        files=files,
        headers={'Authorization': 'Bearer your-token-here'}  # You'll need a real token
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")