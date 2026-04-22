import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatUI.css';

/**
 * ChatUI Component - Right-side conversational interface
 * Handles real-time chat with LangGraph agent
 */
const ChatUI = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Hello! I\'m your CRM-HCP assistant. How can I help you today?',
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  /**
   * Auto-scroll to bottom when new messages arrive
   */
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  /**
   * Scroll to bottom of messages
   */
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  /**
   * Handle message submission
   */
  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!inputValue.trim()) {
      return;
    }

    // Add user message to chat
    const userMessage = {
      id: messages.length + 1,
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // Send message to backend
      const response = await axios.post('http://localhost:8000/api/chat', {
        user_id: 'user_123', // Replace with actual user ID
        message: inputValue,
        conversation_id: conversationId,
        context: {
          timestamp: new Date().toISOString(),
        },
      });

      // Set conversation ID if not set
      if (!conversationId) {
        setConversationId(response.data.conversation_id);
      }

      // Add assistant response to chat
      const assistantMessage = {
        id: messages.length + 2,
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date(response.data.timestamp),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to send message';
      setError(errorMessage);
      console.error('Chat error:', err);

      // Add error message to chat
      const errorMsgObj = {
        id: messages.length + 2,
        role: 'system',
        content: `Error: ${errorMessage}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsgObj]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  /**
   * Handle key press (Enter to send)
   */
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  /**
   * Clear chat history
   */
  const handleClearChat = () => {
    if (window.confirm('Are you sure you want to clear the chat history?')) {
      setMessages([
        {
          id: 1,
          role: 'assistant',
          content: 'Chat cleared. How can I help you?',
          timestamp: new Date(),
        },
      ]);
      setConversationId(null);
      setError(null);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>AI Assistant</h2>
        <button className="clear-button" onClick={handleClearChat} title="Clear chat history">
          Clear
        </button>
      </div>

      {error && <div className="chat-error">{error}</div>}

      <div className="chat-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message message-${message.role}`}>
            <div className="message-content">
              <div className="message-text">{message.content}</div>
              <div className="message-time">
                {message.timestamp.toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message message-loading">
            <div className="message-content">
              <div className="loading-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className="chat-input-form">
        <div className="input-group">
          <textarea
            ref={inputRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here... (Shift+Enter for new line)"
            rows="3"
            disabled={isLoading}
            className="chat-textarea"
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </form>

      {conversationId && (
        <div className="chat-info">
          Conversation ID: {conversationId.substring(0, 20)}...
        </div>
      )}
    </div>
  );
};

export default ChatUI;