import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Send, ArrowLeft, Bot, User } from 'lucide-react';
import axios from 'axios';

const Chat = () => {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchChatHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchChatHistory = async () => {
    try {
      const response = await axios.get('/api/chat/history');
      setMessages(response.data.reverse());
    } catch (error) {
      console.error('Failed to fetch chat history:', error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    const userMessage = { message: newMessage, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await axios.post('/api/chat/message', { message: newMessage });
      setMessages(prev => [...prev, response.data]);
      setNewMessage('');
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link to="/dashboard" className="mr-4">
                <ArrowLeft className="h-5 w-5" />
              </Link>
              <h1 className="text-xl font-semibold">Health Assistant Chat</h1>
            </div>
            <div className="flex items-center">
              <span className="text-gray-700">{user?.full_name}</span>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex-1 max-w-4xl mx-auto w-full flex flex-col">
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-8">
              <Bot className="h-12 w-12 mx-auto mb-4 text-gray-400" />
              <p>Start a conversation with your health assistant!</p>
              <p className="text-sm mt-2">Ask about vaccines, outbreaks, or health information in your area.</p>
            </div>
          )}
          
          {messages.map((message, index) => (
            <div key={index} className="flex items-start space-x-3">
              <div className="flex-shrink-0">
                {message.response ? (
                  <Bot className="h-8 w-8 text-blue-500" />
                ) : (
                  <User className="h-8 w-8 text-gray-500" />
                )}
              </div>
              <div className="flex-1">
                <div className={`rounded-lg p-3 ${
                  message.response 
                    ? 'bg-blue-50 border border-blue-200' 
                    : 'bg-gray-100 border border-gray-200'
                }`}>
                  <p className="text-sm text-gray-900">
                    {message.response || message.message}
                  </p>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}
          
          {loading && (
            <div className="flex items-start space-x-3">
              <Bot className="h-8 w-8 text-blue-500" />
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <div className="border-t bg-white p-4">
          <form onSubmit={sendMessage} className="flex space-x-3">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Ask about health information, vaccines, or outbreaks..."
              className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !newMessage.trim()}
              className="bg-blue-600 text-white rounded-lg px-4 py-2 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="h-5 w-5" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Chat;