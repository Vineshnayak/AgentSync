import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { 
  Activity, Play, Server, TerminalSquare, Clock, AlertTriangle, 
  Layers, Search, Bell, User, LayoutDashboard, AlertCircle, 
  Settings, History, MessageSquare, Send, ChevronRight, CheckCircle2,
  Cpu, FileTerminal, ShieldAlert, Database, Network
} from 'lucide-react';
import './App.css';

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [currentView, setCurrentView] = useState("active_incidents");

  // Incident Workflow State
  const [requestText, setRequestText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [activeTab, setActiveTab] = useState("plan");
  
  // Follow-up chat state
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");
  const [chatActive, setChatActive] = useState(false);
  const [isChatting, setIsChatting] = useState(false);
  const chatEndRef = useRef(null);

  // Agent Fleet State
  const [agents, setAgents] = useState([]);
  
  // History State
  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  // Fetch Agents
  const fetchAgents = async () => {
    try {
      const res = await axios.get(`${API_BASE}/agents`);
      setAgents(res.data.agents || []);
    } catch (e) {
      console.error(e);
    }
  };

  // Fetch History
  const fetchHistory = async () => {
    setHistoryLoading(true);
    try {
      const res = await axios.get(`${API_BASE}/incidents/history`);
      setHistory(res.data.history || []);
    } catch (e) {
      console.error(e);
    } finally {
      setHistoryLoading(false);
    }
  };

  useEffect(() => {
    if (currentView === "agent_fleet") fetchAgents();
    if (currentView === "history") fetchHistory();
  }, [currentView]);

  const runWorkflow = async () => {
    if (!requestText.trim()) return;

    setLoading(true);
    setResult(null);
    setChatActive(false);
    setChatMessages([]);
    setActiveTab("plan");

    try {
      const res = await axios.post(`${API_BASE}/workflow/run`, {
        request_text: requestText
      });
      setResult(res.data);
      setJobId(res.data.job_id);
      setChatMessages([
        { role: 'ai', content: res.data.decision || "Workflow complete. How would you like to proceed with this resolution?" }
      ]);
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

  const handleSendChat = async () => {
    if (!chatInput.trim() || !jobId) return;
    const msg = chatInput;
    setChatMessages(prev => [...prev, { role: 'user', content: msg }]);
    setChatInput("");
    setIsChatting(true);
    
    try {
      const res = await axios.post(`${API_BASE}/workflow/chat/${jobId}`, {
        message: msg
      });
      setChatMessages(prev => [...prev, { role: 'ai', content: res.data.reply }]);
    } catch (error) {
      setChatMessages(prev => [...prev, { role: 'ai', content: "**Error**: Unable to reach resolution agent." }]);
    } finally {
      setIsChatting(false);
    }
  };

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatMessages, chatActive, isChatting]);

  return (
    <div className="layout">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-icon">
            <Layers size={24} color="#6366f1" />
          </div>
          <span className="brand-text">AgentSync</span>
        </div>
        
        <nav className="sidebar-nav">
          <div className="nav-group">Main Menu</div>
          <a href="#" className={`nav-item ${currentView === 'dashboard' ? 'active' : ''}`} onClick={() => setCurrentView('dashboard')}><LayoutDashboard size={20} /> Dashboard</a>
          <a href="#" className={`nav-item ${currentView === 'active_incidents' ? 'active' : ''}`} onClick={() => setCurrentView('active_incidents')}><AlertCircle size={20} /> Active Incidents</a>
          <a href="#" className={`nav-item ${currentView === 'history' ? 'active' : ''}`} onClick={() => setCurrentView('history')}><History size={20} /> Investigations</a>
          
          <div className="nav-group" style={{marginTop: '2rem'}}>System</div>
          <a href="#" className={`nav-item ${currentView === 'agent_fleet' ? 'active' : ''}`} onClick={() => setCurrentView('agent_fleet')}><Cpu size={20} /> Agent Fleet</a>
          <a href="#" className="nav-item"><Settings size={20} /> Settings</a>
        </nav>

        <div className="sidebar-footer">
          <div className="system-status">
            <div className="status-dot healthy"></div>
            <span>System Healthy</span>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        {/* Top Header */}
        <header className="topbar">
          <div className="breadcrumbs">
            <span>AgentSync</span> <ChevronRight size={14} /> <span className="current">
              {currentView === 'dashboard' && "Platform Dashboard"}
              {currentView === 'active_incidents' && "Incident Resolution Center"}
              {currentView === 'history' && "Investigation History"}
              {currentView === 'agent_fleet' && "Agent Fleet Status"}
            </span>
          </div>
          <div className="topbar-actions">
            <div className="search-box">
              <Search size={16} />
              <input type="text" placeholder="Search resources..." />
            </div>
            <button className="icon-btn"><Bell size={20} /></button>
            <div className="user-profile">
              <User size={20} />
            </div>
          </div>
        </header>

        {/* Dashboard Body */}
        <div className="dashboard-body">
          
          {/* Dashboard View */}
          {currentView === 'dashboard' && (
             <div className="view-container">
               <h1 className="page-title">Platform Overview</h1>
               <p className="page-subtitle">Real-time telemetry and Agent metrics</p>
               
               <div className="metrics-grid" style={{ marginTop: '24px' }}>
                 <div className="metric-box">
                    <Database size={24} className="metric-icon" color="#58a6ff" />
                    <div>
                      <div className="metric-val">4</div>
                      <div className="metric-label">Active Agents</div>
                    </div>
                 </div>
                 <div className="metric-box">
                    <CheckCircle2 size={24} className="metric-icon" color="#3fb950" />
                    <div>
                      <div className="metric-val">128</div>
                      <div className="metric-label">Incidents Resolved</div>
                    </div>
                 </div>
                 <div className="metric-box">
                    <Network size={24} className="metric-icon" color="#a371f7" />
                    <div>
                      <div className="metric-val">99.9%</div>
                      <div className="metric-label">System Uptime</div>
                    </div>
                 </div>
               </div>
             </div>
          )}

          {/* Active Incidents View */}
          {currentView === 'active_incidents' && (
            <div className="view-container">
              <div className="page-header">
                <div>
                  <h1 className="page-title">Incident Resolution Center</h1>
                  <p className="page-subtitle">Multi-agent orchestration for complex system failures</p>
                </div>
                {result && (
                  <div className={`status-badge ${result.status?.includes('Error') ? 'error' : 'success'}`}>
                    {result.status?.includes('Error') ? <ShieldAlert size={16} /> : <CheckCircle2 size={16} />}
                    {result.status}
                  </div>
                )}
              </div>

              <div className="grid-layout">
                {/* Left Column: Input and Results */}
                <div className="left-column">
                  <div className="card input-card">
                    <div className="card-header">
                      <h3><FileTerminal size={18} /> Initialize Investigation</h3>
                    </div>
                    <div className="card-body">
                      <textarea
                        className="enterprise-textarea"
                        rows={3}
                        placeholder="Describe the incident (e.g. Payment API is returning 500 errors...)"
                        value={requestText}
                        onChange={(e) => setRequestText(e.target.value)}
                      />
                      <div className="action-row">
                        <button className="btn-primary" onClick={runWorkflow} disabled={loading || !requestText.trim()}>
                          {loading ? <Activity className="spinner" size={18} /> : <Play size={18} />}
                          {loading ? "Agents Orchestrating..." : "Run Analysis"}
                        </button>
                      </div>
                    </div>
                  </div>

                  {loading && !result && (
                    <div className="loading-state card">
                      <Activity className="spinner" size={40} color="#6366f1" />
                      <h3>Coordinating Agent Fleet</h3>
                      <p>Executing planning, investigation, and analysis phases.</p>
                    </div>
                  )}

                  {result && (
                    <div className="results-container">
                      <div className="metrics-grid">
                        <div className="metric-box">
                          <Clock size={20} className="metric-icon" />
                          <div>
                            <div className="metric-val">{result.execution_metrics?.duration_seconds || 0}s</div>
                            <div className="metric-label">Execution Time</div>
                          </div>
                        </div>
                        <div className="metric-box">
                          <Server size={20} className="metric-icon" />
                          <div>
                            <div className="metric-val">{result.execution_metrics?.llm_calls || 0}</div>
                            <div className="metric-label">LLM Calls</div>
                          </div>
                        </div>
                        <div className="metric-box">
                          <TerminalSquare size={20} className="metric-icon" />
                          <div>
                            <div className="metric-val">{result.execution_metrics?.tool_calls || 0}</div>
                            <div className="metric-label">Tool Invocations</div>
                          </div>
                        </div>
                      </div>

                      <div className="card tabs-card">
                        <div className="tabs-header">
                          <button className={`tab-btn ${activeTab === 'plan' ? 'active' : ''}`} onClick={() => setActiveTab('plan')}>Execution Plan</button>
                          <button className={`tab-btn ${activeTab === 'investigation' ? 'active' : ''}`} onClick={() => setActiveTab('investigation')}>Investigation</button>
                          <button className={`tab-btn ${activeTab === 'analysis' ? 'active' : ''}`} onClick={() => setActiveTab('analysis')}>Analysis</button>
                          <button className={`tab-btn ${activeTab === 'decision' ? 'active' : ''}`} onClick={() => setActiveTab('decision')}>Recommendation</button>
                        </div>
                        <div className="tab-content markdown-body">
                          {activeTab === 'plan' && <ReactMarkdown remarkPlugins={[remarkGfm]}>{result.plan || "No data."}</ReactMarkdown>}
                          {activeTab === 'investigation' && <ReactMarkdown remarkPlugins={[remarkGfm]}>{result.investigation_results || "No data."}</ReactMarkdown>}
                          {activeTab === 'analysis' && <ReactMarkdown remarkPlugins={[remarkGfm]}>{result.analysis || "No data."}</ReactMarkdown>}
                          {activeTab === 'decision' && <ReactMarkdown remarkPlugins={[remarkGfm]}>{result.decision || "No data."}</ReactMarkdown>}
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Right Column: Follow-up Chat */}
                <div className="right-column">
                  {result && !chatActive && (
                    <div className="resolution-prompt card">
                      <div className="prompt-icon"><MessageSquare size={32} /></div>
                      <h3>Follow-up & Resolution</h3>
                      <p>Would you like to execute the recommendation or investigate further?</p>
                      <button className="btn-secondary" onClick={() => setChatActive(true)}>
                        Open Resolution Chat <ChevronRight size={16} />
                      </button>
                    </div>
                  )}

                  {chatActive && (
                    <div className="chat-interface card">
                      <div className="chat-header">
                        <h4>Resolution Copilot</h4>
                        <span className="badge">Active</span>
                      </div>
                      <div className="chat-messages">
                        {chatMessages.map((msg, idx) => (
                          <div key={idx} className={`message-bubble ${msg.role}`}>
                            {msg.role === 'ai' && <div className="avatar"><Layers size={14} /></div>}
                            <div className="msg-content">
                              <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                            </div>
                          </div>
                        ))}
                        {isChatting && (
                          <div className="message-bubble ai">
                            <div className="avatar"><Layers size={14} /></div>
                            <div className="msg-content">
                              <span className="typing-dots">Agent is thinking...</span>
                            </div>
                          </div>
                        )}
                        <div ref={chatEndRef} />
                      </div>
                      <div className="chat-input-area">
                        <input 
                          type="text" 
                          placeholder="Instruct the agents to fix the issue..." 
                          value={chatInput}
                          onChange={(e) => setChatInput(e.target.value)}
                          onKeyDown={(e) => e.key === 'Enter' && handleSendChat()}
                          disabled={isChatting}
                        />
                        <button className="send-btn" onClick={handleSendChat} disabled={!chatInput.trim() || isChatting}>
                          <Send size={18} />
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* History View */}
          {currentView === 'history' && (
            <div className="view-container">
              <h1 className="page-title">Investigations Log</h1>
              <p className="page-subtitle">History of previous incident workflows stored in database</p>
              
              <div className="card" style={{ marginTop: '24px' }}>
                <div className="table-responsive">
                  <table className="enterprise-table">
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>User Request</th>
                        <th>Timestamp</th>
                        <th>Final Decision</th>
                      </tr>
                    </thead>
                    <tbody>
                      {historyLoading ? (
                        <tr><td colSpan="4" style={{ textAlign: 'center', padding: '24px' }}><Activity className="spinner" size={24} color="#6366f1" /></td></tr>
                      ) : history.length === 0 ? (
                        <tr><td colSpan="4" style={{ textAlign: 'center', padding: '24px' }}>No investigations found in database.</td></tr>
                      ) : (
                        history.map((record) => (
                          <tr key={record.id}>
                            <td>#{record.id}</td>
                            <td className="truncate-cell"><strong>{record.user_request}</strong></td>
                            <td>{new Date(record.timestamp + 'Z').toLocaleString()}</td>
                            <td className="truncate-cell">{record.decision}</td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* Agent Fleet View */}
          {currentView === 'agent_fleet' && (
            <div className="view-container">
              <h1 className="page-title">Agent Fleet Operations</h1>
              <p className="page-subtitle">Current status of autonomous agents across the network</p>
              
              <div className="agents-grid" style={{ marginTop: '24px', display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
                {agents.map((agent) => (
                  <div key={agent.id} className="card agent-card">
                    <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <h3><Cpu size={18} /> {agent.name}</h3>
                      <span className="status-badge success"><span className="status-dot healthy" style={{marginRight: '6px'}}></span> {agent.status}</span>
                    </div>
                    <div className="card-body">
                      <p style={{ color: 'var(--text-muted)', fontSize: '14px', lineHeight: '1.5' }}>{agent.description}</p>
                    </div>
                  </div>
                ))}
                {agents.length === 0 && <p>Loading agents from backend API...</p>}
              </div>
            </div>
          )}

        </div>
      </main>
    </div>
  );
}

export default App;
