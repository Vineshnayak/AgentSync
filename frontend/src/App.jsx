import { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, Play, CheckCircle, AlertTriangle, Clock, Server, TerminalSquare, RefreshCw, Layers } from 'lucide-react';
import './App.css';

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [requestText, setRequestText] = useState("");
  const [loading, setLoading] = useState(false);
  const [jobId, setJobId] = useState(null);
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState("plan");

  const runWorkflow = async () => {
    if (!requestText.trim()) return;
    
    setLoading(true);
    setResult(null);
    setJobId(null);
    setActiveTab("plan");
    
    try {
      const res = await axios.post(`${API_BASE}/workflow/run`, {
        request_text: requestText
      });
      // The API currently runs synchronously and returns the full result immediately
      setResult(res.data);
    } catch (error) {
      console.error("Workflow failed", error);
      setResult({
        status: "Error",
        errors: [error.response?.data?.detail || error.message]
      });
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    if (!status) return null;
    let cls = "status-running";
    if (status.includes("Complete") || status.includes("Low Risk")) cls = "status-completed";
    if (status.includes("Error") || status.includes("High Risk")) cls = "status-error";
    
    return <div className={`status-badge ${cls}`}>{status}</div>;
  };

  return (
    <div className="app-container">
      <header className="header">
        <Layers size={40} className="header-icon" />
        <div>
          <h1>AgentSync Orchestration Engine</h1>
          <p>Enterprise multi-agent IT incident resolution platform</p>
        </div>
        {result && getStatusBadge(result.status)}
      </header>

      <div className="glass-panel input-section">
        <label htmlFor="incident">Incident Description</label>
        <textarea
          id="incident"
          className="textarea-custom"
          rows={4}
          placeholder="e.g. The Payment API is returning 500 internal server errors causing checkout failures..."
          value={requestText}
          onChange={(e) => setRequestText(e.target.value)}
        />
        <button 
          className="btn-primary" 
          onClick={runWorkflow}
          disabled={loading || !requestText.trim()}
        >
          {loading ? <RefreshCw className="spinner" size={18} /> : <Play size={18} />}
          {loading ? "Orchestrating Agents..." : "Initialize Resolution Workflow"}
        </button>
      </div>

      {loading && !result && (
        <div className="loading-state">
          <RefreshCw className="spinner" size={48} />
          <h2>Agents coordinating...</h2>
          <p>Executing Planning, Investigation, and Analysis phases in real-time.</p>
        </div>
      )}

      {result && (
        <div className="glass-panel results-grid">
          
          <div className="metrics-row">
            <div className="metric-card">
              <Clock className="header-icon" size={24} style={{marginBottom: "0.5rem"}} />
              <div className="metric-value">{result.execution_metrics?.duration_seconds || 0}s</div>
              <div className="metric-label">Execution Time</div>
            </div>
            <div className="metric-card">
              <Server className="header-icon" size={24} style={{marginBottom: "0.5rem"}} />
              <div className="metric-value">{result.execution_metrics?.llm_calls || 0}</div>
              <div className="metric-label">LLM Operations</div>
            </div>
            <div className="metric-card">
              <TerminalSquare className="header-icon" size={24} style={{marginBottom: "0.5rem"}} />
              <div className="metric-value">{result.execution_metrics?.tool_calls || 0}</div>
              <div className="metric-label">Tool Invocations</div>
            </div>
          </div>

          {result.errors && result.errors.length > 0 && (
            <div style={{color: '#f87171', padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px'}}>
              <h3 style={{marginTop: 0}}><AlertTriangle size={20} style={{marginRight: '8px', verticalAlign: 'middle'}}/> Workflow Errors</h3>
              <ul style={{margin: 0}}>
                {result.errors.map((err, i) => <li key={i}>{err}</li>)}
              </ul>
            </div>
          )}

          <div>
            <div className="tabs-container">
              <button className={`tab-btn ${activeTab === 'plan' ? 'active' : ''}`} onClick={() => setActiveTab('plan')}>
                Execution Plan
              </button>
              <button className={`tab-btn ${activeTab === 'investigation' ? 'active' : ''}`} onClick={() => setActiveTab('investigation')}>
                Investigation Data
              </button>
              <button className={`tab-btn ${activeTab === 'analysis' ? 'active' : ''}`} onClick={() => setActiveTab('analysis')}>
                Technical Analysis
              </button>
              <button className={`tab-btn ${activeTab === 'decision' ? 'active' : ''}`} onClick={() => setActiveTab('decision')}>
                Final Recommendation
              </button>
            </div>

            <div className="tab-content">
              {activeTab === 'plan' && <pre>{result.plan || "No plan generated."}</pre>}
              {activeTab === 'investigation' && <pre>{result.investigation_results || "No investigation data."}</pre>}
              {activeTab === 'analysis' && <pre>{result.analysis || "No analysis generated."}</pre>}
              {activeTab === 'decision' && <pre>{result.decision || "No decision formulated."}</pre>}
            </div>
          </div>

        </div>
      )}
    </div>
  );
}

export default App;
