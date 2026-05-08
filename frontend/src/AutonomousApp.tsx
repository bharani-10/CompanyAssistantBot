import React, { useState, useEffect } from 'react';
import { 
  Database, Upload, Play, BarChart3, FileText, Zap, AlertCircle, Clock, CheckCircle, 
  Loader, TrendingUp, Brain, Cpu, Activity, Code, GitBranch, Download, Eye, 
  Rocket, Settings, Terminal, Globe, Package, FolderOpen, File
} from 'lucide-react';

interface AgentStatus {
  agent: string;
  status: string;
  phase?: string;
  data?: any;
  timestamp: number;
}

interface GeneratedProject {
  id: string;
  path: string;
  metadata: any;
}

function AutonomousApp() {
  const [activeView, setActiveView] = useState('mission-control');
  const [isGenerating, setIsGenerating] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);
  const [userPrompt, setUserPrompt] = useState('');
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const [agentLogs, setAgentLogs] = useState<AgentStatus[]>([]);
  const [currentPhase, setCurrentPhase] = useState<string>('');
  const [generationComplete, setGenerationComplete] = useState(false);
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [generatedProjects, setGeneratedProjects] = useState<GeneratedProject[]>([]);
  const [selectedProject, setSelectedProject] = useState<GeneratedProject | null>(null);

  // WebSocket connection for real-time updates
  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8000/ws');
    
    websocket.onopen = () => {
      console.log('🔗 Autonomous WebSocket connected');
      setWs(websocket);
    };
    
    websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('📡 Autonomous update:', data);
        
        const newLog: AgentStatus = {
          agent: data.agent,
          status: data.status,
          phase: data.phase,
          data: data.data,
          timestamp: Date.now()
        };
        
        setAgentLogs(prev => [...prev, newLog]);
        setCurrentPhase(data.phase || '');
        
        // Check if generation is complete
        if (data.phase === 'complete') {
          setGenerationComplete(true);
          setIsGenerating(false);
          loadGeneratedProjects();
        }
      } catch (error) {
        console.error('WebSocket message error:', error);
      }
    };
    
    return () => {
      websocket.close();
    };
  }, []);

  // Load generated projects
  const loadGeneratedProjects = async () => {
    try {
      const response = await fetch('http://localhost:8000/projects');
      if (response.ok) {
        const data = await response.json();
        setGeneratedProjects(data.projects);
      }
    } catch (error) {
      console.error('Failed to load projects:', error);
    }
  };

  useEffect(() => {
    loadGeneratedProjects();
  }, []);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.csv')) {
      setUploadStatus('❌ Please select a CSV file');
      return;
    }

    setUploadStatus('📤 Uploading dataset...');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        const result = await response.json();
        setUploadedFile(result.path);
        setUploadStatus(`✅ Dataset uploaded: ${result.filename}`);
      } else {
        setUploadStatus('❌ Upload failed');
      }
    } catch (error) {
      setUploadStatus('❌ Upload failed - Check backend connection');
    }
  };

  const handleStartAutonomousGeneration = async () => {
    if (!uploadedFile || !userPrompt.trim()) {
      setUploadStatus('❌ Please upload dataset and enter project description');
      return;
    }

    setIsGenerating(true);
    setGenerationComplete(false);
    setAgentLogs([]);
    setUploadStatus('🚀 Autonomous AI Swarm Engaged...');
    setActiveView('agent-theater');

    try {
      const response = await fetch(`http://localhost:8000/generate-complete-project?dataset_path=${encodeURIComponent(uploadedFile)}&user_prompt=${encodeURIComponent(userPrompt)}`, {
        method: 'POST',
      });
      
      if (response.ok) {
        setUploadStatus('✅ Autonomous generation started!');
      } else {
        setUploadStatus('❌ Generation failed to start');
        setIsGenerating(false);
      }
    } catch (error) {
      setUploadStatus('❌ Generation failed - Check backend connection');
      setIsGenerating(false);
    }
  };

  const getPhaseIcon = (phase: string) => {
    switch (phase) {
      case 'initialization': return <Rocket className="w-4 h-4" />;
      case 'analysis': return <Brain className="w-4 h-4" />;
      case 'architecture': return <Cpu className="w-4 h-4" />;
      case 'generation': return <Code className="w-4 h-4" />;
      case 'execution': return <Play className="w-4 h-4" />;
      case 'debugging': return <Settings className="w-4 h-4" />;
      case 'deployment': return <Package className="w-4 h-4" />;
      case 'complete': return <CheckCircle className="w-4 h-4" />;
      default: return <Activity className="w-4 h-4" />;
    }
  };

  const getPhaseColor = (phase: string) => {
    switch (phase) {
      case 'initialization': return 'text-blue-400';
      case 'analysis': return 'text-cyan-400';
      case 'architecture': return 'text-purple-400';
      case 'generation': return 'text-yellow-400';
      case 'execution': return 'text-green-400';
      case 'debugging': return 'text-orange-400';
      case 'deployment': return 'text-pink-400';
      case 'complete': return 'text-emerald-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="w-screen h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-black text-white overflow-hidden">
      {/* Futuristic Header */}
      <header className="bg-black/40 backdrop-blur-xl border-b border-cyan-400/30 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Brain className="w-8 h-8 text-cyan-400 animate-pulse" />
              <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                MetaMind OS
              </h1>
            </div>
            <div className="text-xs text-gray-400 font-mono">
              AUTONOMOUS AI SOFTWARE ENGINEERING SYSTEM
            </div>
          </div>
          
          <div className="flex space-x-2">
            <button 
              onClick={() => setActiveView('mission-control')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeView === 'mission-control' 
                  ? 'bg-cyan-400/20 text-cyan-400 border border-cyan-400/30' 
                  : 'text-gray-300 hover:text-white hover:bg-white/5'
              }`}
            >
              <Rocket className="inline w-4 h-4 mr-2" />
              Mission Control
            </button>
            <button 
              onClick={() => setActiveView('agent-theater')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeView === 'agent-theater' 
                  ? 'bg-purple-400/20 text-purple-400 border border-purple-400/30' 
                  : 'text-gray-300 hover:text-white hover:bg-white/5'
              }`}
            >
              <Brain className="inline w-4 h-4 mr-2" />
              Agent Theater
            </button>
            <button 
              onClick={() => setActiveView('project-center')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeView === 'project-center' 
                  ? 'bg-green-400/20 text-green-400 border border-green-400/30' 
                  : 'text-gray-300 hover:text-white hover:bg-white/5'
              }`}
            >
              <FolderOpen className="inline w-4 h-4 mr-2" />
              Project Center
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="h-full overflow-hidden">
        {activeView === 'mission-control' && (
          <div className="h-full p-8 overflow-y-auto">
            <div className="max-w-6xl mx-auto">
              <h2 className="text-4xl font-bold mb-2 bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                Autonomous Project Generation
              </h2>
              <p className="text-gray-400 mb-8 text-lg">
                Upload a dataset and describe your vision. MetaMind will autonomously generate a complete production-ready ML application.
              </p>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Dataset Upload */}
                <div className="bg-black/20 backdrop-blur-xl border border-cyan-400/20 rounded-xl p-8">
                  <h3 className="text-2xl font-semibold mb-6 flex items-center text-cyan-400">
                    <Upload className="w-6 h-6 mr-3" />
                    Dataset Upload
                  </h3>
                  
                  {/* Quick Test */}
                  <div className="mb-6 p-4 bg-blue-900/20 border border-blue-400/20 rounded-lg">
                    <h4 className="text-sm font-medium text-blue-400 mb-2">🚀 Quick Demo</h4>
                    <button
                      onClick={() => {
                        setUploadedFile('data/students_performance.csv');
                        setUploadStatus('✅ Demo dataset loaded: students_performance.csv');
                      }}
                      className="bg-blue-500/20 hover:bg-blue-500/40 border border-blue-400/30 px-4 py-2 rounded text-sm transition-all"
                    >
                      Use Demo Dataset
                    </button>
                  </div>

                  <div className="border-2 border-dashed border-cyan-400/40 rounded-xl p-8 text-center hover:border-cyan-400/60 transition-all">
                    <Upload className="w-16 h-16 text-cyan-400 mx-auto mb-4 opacity-60" />
                    <h4 className="text-lg font-semibold mb-2">Upload CSV Dataset</h4>
                    <p className="text-gray-400 mb-4">MetaMind will analyze and build a complete ML application</p>
                    <input
                      type="file"
                      accept=".csv"
                      onChange={handleFileUpload}
                      className="hidden"
                      id="file-upload"
                    />
                    <label
                      htmlFor="file-upload"
                      className="bg-cyan-500/20 hover:bg-cyan-500/40 border border-cyan-400/30 px-6 py-3 rounded-lg cursor-pointer inline-block transition-all"
                    >
                      Select Dataset
                    </label>
                  </div>
                  
                  {uploadStatus && (
                    <div className={`mt-4 p-4 rounded-lg border-l-4 ${
                      uploadStatus.includes('✅') ? 'bg-green-900/20 border-green-400' :
                      uploadStatus.includes('❌') ? 'bg-red-900/20 border-red-400' :
                      'bg-blue-900/20 border-cyan-400'
                    }`}>
                      <p className="text-sm font-mono">{uploadStatus}</p>
                    </div>
                  )}
                </div>

                {/* Project Description */}
                <div className="bg-black/20 backdrop-blur-xl border border-purple-400/20 rounded-xl p-8">
                  <h3 className="text-2xl font-semibold mb-6 flex items-center text-purple-400">
                    <FileText className="w-6 h-6 mr-3" />
                    Project Vision
                  </h3>
                  
                  {/* Quick Prompts */}
                  <div className="mb-6 p-4 bg-purple-900/20 border border-purple-400/20 rounded-lg">
                    <h4 className="text-sm font-medium text-purple-400 mb-3">🎯 Example Visions</h4>
                    <div className="grid grid-cols-1 gap-2">
                      <button
                        onClick={() => setUserPrompt('Build a complete student performance prediction system with a modern web interface, API endpoints, and deployment-ready configuration. Include data visualization, model explanations, and batch prediction capabilities.')}
                        className="bg-purple-600/20 hover:bg-purple-600/40 px-3 py-2 rounded text-xs text-left border border-purple-400/20 transition-all"
                      >
                        📚 Student Performance Prediction Platform
                      </button>
                      <button
                        onClick={() => setUserPrompt('Create a production-ready customer churn prediction application with real-time predictions, interactive dashboards, model monitoring, and automated retraining capabilities.')}
                        className="bg-purple-600/20 hover:bg-purple-600/40 px-3 py-2 rounded text-xs text-left border border-purple-400/20 transition-all"
                      >
                        👥 Customer Churn Prevention System
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-3">
                      Describe your complete ML application vision:
                    </label>
                    <textarea
                      value={userPrompt}
                      onChange={(e) => setUserPrompt(e.target.value)}
                      placeholder="Example: Build a complete fraud detection system with real-time API, interactive dashboard, model monitoring, automated alerts, and deployment configuration for production use."
                      className="w-full h-40 bg-gray-800/50 border border-gray-600/50 rounded-lg p-4 text-white placeholder-gray-400 focus:border-purple-400 focus:outline-none resize-none"
                    />
                  </div>
                  
                  <div className="mt-6 text-sm text-gray-400">
                    <p className="mb-2">🤖 <strong>MetaMind will autonomously generate:</strong></p>
                    <ul className="list-disc list-inside space-y-1 ml-4 text-xs">
                      <li>Complete FastAPI backend with ML endpoints</li>
                      <li>Modern React frontend with dashboards</li>
                      <li>ML training pipeline with best practices</li>
                      <li>Docker deployment configuration</li>
                      <li>GitHub repository with documentation</li>
                    </ul>
                  </div>
                </div>
              </div>

              {/* Launch Button */}
              <div className="mt-8 text-center">
                <button
                  onClick={handleStartAutonomousGeneration}
                  disabled={!uploadedFile || !userPrompt.trim() || isGenerating}
                  className={`px-12 py-4 rounded-xl font-bold text-lg transition-all ${
                    uploadedFile && userPrompt.trim() && !isGenerating
                      ? 'bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-400 hover:to-purple-400 text-white shadow-lg shadow-cyan-500/25'
                      : 'bg-gray-600/50 text-gray-400 cursor-not-allowed'
                  }`}
                >
                  {isGenerating ? (
                    <div className="flex items-center">
                      <Loader className="w-6 h-6 mr-3 animate-spin" />
                      Autonomous Swarm Active...
                    </div>
                  ) : (
                    <div className="flex items-center">
                      <Rocket className="w-6 h-6 mr-3" />
                      Launch Autonomous Generation
                    </div>
                  )}
                </button>
                
                {(!uploadedFile || !userPrompt.trim()) && (
                  <div className="mt-4 flex items-center justify-center text-yellow-400 text-sm">
                    <AlertCircle className="w-4 h-4 mr-2" />
                    Complete dataset upload and project vision to launch
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeView === 'agent-theater' && (
          <div className="h-full p-8 overflow-y-auto">
            <div className="max-w-7xl mx-auto">
              <h2 className="text-4xl font-bold mb-8 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                Autonomous Agent Theater
              </h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Current Phase */}
                <div className="bg-black/20 backdrop-blur-xl border border-green-400/20 rounded-xl p-6">
                  <h3 className="text-xl font-semibold mb-4 flex items-center text-green-400">
                    <Activity className="w-5 h-5 mr-2" />
                    Current Phase
                  </h3>
                  
                  {isGenerating ? (
                    <div className="text-center py-6">
                      <div className={`${getPhaseColor(currentPhase)} mb-4`}>
                        {getPhaseIcon(currentPhase)}
                      </div>
                      <Loader className="w-8 h-8 text-green-400 mx-auto mb-3 animate-spin" />
                      <p className="text-green-400 font-medium capitalize">{currentPhase || 'Initializing'}</p>
                      <p className="text-sm text-gray-400 mt-2">Autonomous agents working...</p>
                    </div>
                  ) : generationComplete ? (
                    <div className="text-center py-6">
                      <CheckCircle className="w-8 h-8 text-emerald-400 mx-auto mb-3" />
                      <p className="text-emerald-400 font-medium">Generation Complete!</p>
                      <p className="text-sm text-gray-400 mt-2">Project ready for deployment</p>
                    </div>
                  ) : (
                    <div className="text-center py-6">
                      <Clock className="w-8 h-8 text-gray-400 mx-auto mb-3" />
                      <p className="text-gray-400">Awaiting mission launch</p>
                    </div>
                  )}
                </div>

                {/* Agent Timeline */}
                <div className="lg:col-span-2 bg-black/20 backdrop-blur-xl border border-cyan-400/20 rounded-xl p-6">
                  <h3 className="text-xl font-semibold mb-4 flex items-center text-cyan-400">
                    <Terminal className="w-5 h-5 mr-2" />
                    Agent Activity Stream
                  </h3>
                  
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {agentLogs.length === 0 ? (
                      <div className="text-center py-8 text-gray-400">
                        <Brain className="w-12 h-12 mx-auto mb-3 opacity-30" />
                        <p>Agent swarm ready for deployment</p>
                      </div>
                    ) : (
                      agentLogs.slice(-15).reverse().map((log, index) => (
                        <div key={index} className="flex items-start space-x-3 p-3 bg-gray-800/30 rounded-lg border border-gray-700/30">
                          <div className={`${getPhaseColor(log.phase || '')} mt-1`}>
                            {getPhaseIcon(log.phase || '')}
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center justify-between mb-1">
                              <span className={`font-medium ${getPhaseColor(log.phase || '')} text-sm`}>
                                {log.agent}
                              </span>
                              <span className="text-gray-500 text-xs font-mono">
                                {new Date(log.timestamp).toLocaleTimeString()}
                              </span>
                            </div>
                            <p className="text-gray-300 text-sm">{log.status}</p>
                            {log.data && (
                              <div className="mt-2 text-xs text-gray-400 bg-gray-900/50 p-2 rounded font-mono">
                                {JSON.stringify(log.data, null, 2).substring(0, 150)}...
                              </div>
                            )}
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeView === 'project-center' && (
          <div className="h-full p-8 overflow-y-auto">
            <div className="max-w-7xl mx-auto">
              <h2 className="text-4xl font-bold mb-8 bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
                Generated Projects
              </h2>
              
              {generatedProjects.length === 0 ? (
                <div className="text-center py-16">
                  <FolderOpen className="w-16 h-16 text-gray-400 mx-auto mb-4 opacity-50" />
                  <p className="text-gray-400 text-lg">No projects generated yet</p>
                  <p className="text-gray-500 text-sm mt-2">Launch autonomous generation to create your first project</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {generatedProjects.map((project) => (
                    <div key={project.id} className="bg-black/20 backdrop-blur-xl border border-gray-400/20 rounded-xl p-6 hover:border-cyan-400/40 transition-all">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-semibold text-white truncate">{project.id}</h3>
                        <div className={`px-2 py-1 rounded text-xs ${
                          project.metadata.status === 'complete' ? 'bg-green-500/20 text-green-400' :
                          project.metadata.status === 'recovery_mode' ? 'bg-yellow-500/20 text-yellow-400' :
                          'bg-gray-500/20 text-gray-400'
                        }`}>
                          {project.metadata.status || 'unknown'}
                        </div>
                      </div>
                      
                      <div className="space-y-2 mb-4">
                        <div className="flex items-center text-sm text-gray-400">
                          <File className="w-4 h-4 mr-2" />
                          Backend: {project.metadata.backend_files || 0} files
                        </div>
                        <div className="flex items-center text-sm text-gray-400">
                          <Globe className="w-4 h-4 mr-2" />
                          Frontend: {project.metadata.frontend_files || 0} files
                        </div>
                        <div className="flex items-center text-sm text-gray-400">
                          <Brain className="w-4 h-4 mr-2" />
                          ML: {project.metadata.ml_files || 0} files
                        </div>
                      </div>
                      
                      <div className="flex space-x-2">
                        <button
                          onClick={() => window.open(`http://localhost:8000/projects/${project.id}/download`, '_blank')}
                          className="flex-1 bg-cyan-500/20 hover:bg-cyan-500/40 border border-cyan-400/30 px-3 py-2 rounded text-sm transition-all flex items-center justify-center"
                        >
                          <Download className="w-4 h-4 mr-2" />
                          Download
                        </button>
                        <button
                          onClick={() => setSelectedProject(project)}
                          className="flex-1 bg-purple-500/20 hover:bg-purple-500/40 border border-purple-400/30 px-3 py-2 rounded text-sm transition-all flex items-center justify-center"
                        >
                          <Eye className="w-4 h-4 mr-2" />
                          Explore
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default AutonomousApp;