import React, { useState, useRef, useEffect } from 'react';
import { sendMessage, ChatApiError } from '../services/chatApi';

export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

export const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const generateId = () => Math.random().toString(36).substr(2, 9);

  const addMessage = (text: string, sender: 'user' | 'bot') => {
    const newMessage: Message = {
      id: generateId(),
      text,
      sender,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setError(null);

    // Add user message
    addMessage(userMessage, 'user');
    setIsLoading(true);

    try {
      // Send message to API
      const response = await sendMessage(userMessage);

      addMessage(response, 'bot');
    } catch (err) {
      let errorMessage = 'Failed to send message. Please try again.';
      
      if (err instanceof ChatApiError) {
        if (err.status === 404) {
          errorMessage = 'Chat service not available. Make sure the server is running on localhost:8000';
        } else if (err.status === 500) {
          errorMessage = 'Server error. Please try again later.';
        } else {
          errorMessage = err.message;
        }
      }
      
      setError(errorMessage);
      addMessage(`Error: ${errorMessage}`, 'bot');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <div className="flex flex-col h-screen max-h-[800px] max-w-4xl mx-auto border border-gray-200 rounded-xl overflow-hidden bg-white shadow-xl">
      <div className="flex justify-between items-center px-5 py-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white border-b border-gray-200">
        <h2 className="m-0 text-xl font-semibold">MCP based AI Chatbot</h2>
        <button 
          onClick={clearChat}
          className="bg-white/20 text-white border border-white/30 px-3 py-1.5 rounded-md cursor-pointer text-sm transition-all duration-200 hover:bg-white/30 disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={messages.length === 0}
        >
          Clear Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-5 bg-gray-50 flex flex-col gap-4 scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-100">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 mt-[50%] transform -translate-y-1/2">
            <p className="my-2">👋 Hello! I'm your AI assistant. Ask me anything!</p>
            <p className="my-2 italic text-gray-400 text-sm">Abilities: Weather, News, Jokes</p>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex mb-3 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className="max-w-[70%] flex flex-col">
                  <div className={`px-4 py-3 rounded-[18px] break-words leading-relaxed ${
                    message.sender === 'user' 
                      ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-br-sm' 
                      : 'bg-white text-gray-800 border border-gray-200 rounded-bl-sm shadow-sm'
                  }`}>
                    {message.text}
                  </div>
                  <div className={`text-xs text-gray-400 mt-1 ${
                    message.sender === 'user' ? 'text-right' : 'text-left'
                  }`}>
                    {message.timestamp.toLocaleTimeString([], { 
                      hour: '2-digit', 
                      minute: '2-digit' 
                    })}
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {error && (
        <div className="flex justify-between items-center bg-red-50 text-red-600 px-5 py-3 border-l-4 border-red-600 mx-5 rounded-r-md">
          <span>⚠️ {error}</span>
          <button 
            onClick={() => setError(null)}
            className="bg-none border-none text-red-600 text-xl cursor-pointer p-0 w-5 h-5 flex items-center justify-center hover:bg-red-100 rounded"
          >
            &times;
          </button>
        </div>
      )}

      <div className="p-5 bg-white border-t border-gray-200">
        <div className="flex gap-3 items-end">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            className="flex-1 min-h-[40px] max-h-[120px] px-4 py-3 border-2 border-gray-200 rounded-[20px] resize-none font-inherit text-base leading-relaxed transition-colors duration-200 outline-none focus:border-indigo-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
            rows={1}
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="w-10 h-10 rounded-full border-none bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-xl cursor-pointer flex items-center justify-center transition-all duration-200 flex-shrink-0 hover:scale-105 hover:shadow-lg hover:shadow-indigo-400/40 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            {isLoading ? (
              <span className="animate-spin inline-block">⟳</span>
            ) : (
              '→'
            )}
          </button>
        </div>
      </div>
    </div>
  );
};