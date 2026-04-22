import React from 'react';
import { Provider } from 'react-redux';
import store from './store/store';
import FormUI from './components/FormUI';
import ChatUI from './components/ChatUI';
import './App.css';

/**
 * Main App Component
 * Combines the structured form interface and conversational chat interface
 */
function App() {
  return (
    <Provider store={store}>
      <div className="app-container">
        <header className="app-header">
          <h1>CRM-HCP Module</h1>
          <p>Customer Relationship Management & Healthcare Provider Integration</p>
        </header>

        <main className="app-main">
          <div className="left-panel">
            <FormUI />
          </div>
          <div className="divider"></div>
          <div className="right-panel">
            <ChatUI />
          </div>
        </main>

        <footer className="app-footer">
          <p>&copy; 2024 CRM-HCP Module. All rights reserved.</p>
        </footer>
      </div>
    </Provider>
  );
}

export default App;