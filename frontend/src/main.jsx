import React, { StrictMode, Component } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an unhandled render error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          background: '#0d1117',
          color: '#f0f6fc',
          fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
          padding: 24,
          textAlign: 'center'
        }}>
          <div style={{
            maxWidth: 520,
            background: 'rgba(22, 27, 34, 0.8)',
            border: '1px solid rgba(248, 81, 73, 0.4)',
            borderRadius: 12,
            padding: 32,
            boxShadow: '0 8px 32px rgba(0,0,0,0.4)'
          }}>
            <div style={{ fontSize: 36, marginBottom: 16 }}>⚠️</div>
            <h2 style={{ margin: '0 0 8px', fontSize: 20, color: '#f85149' }}>Something went wrong</h2>
            <p style={{ margin: '0 0 20px', color: '#8b949e', fontSize: 14, lineHeight: 1.5 }}>
              The application encountered an unexpected display issue. Your data and backend workflows are safe.
            </p>
            <button
              onClick={() => {
                this.setState({ hasError: false });
                window.location.reload();
              }}
              style={{
                background: '#238636',
                color: '#fff',
                border: 'none',
                borderRadius: 6,
                padding: '10px 20px',
                fontWeight: 600,
                fontSize: 14,
                cursor: 'pointer'
              }}
            >
              Reload Platform
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
)
