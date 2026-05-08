import React, { useState } from 'react';
import { Upload, Play, Database, Box, Info, Settings } from 'lucide-react';
import { useMetaMindStore } from '../../store/useMetaMindStore';

export const Sidebar: React.FC = () => {
  const { setDataset, activeDataset, setProcessing, isProcessing, addLog, updateAgent } = useMetaMindStore();
  const [instruction, setInstruction] = useState("Predict student performance based on study hours and attendance.");

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setDataset(data.path);
      addLog({
        agent: "SYSTEM",
        status: `Dataset uploaded: ${data.filename}`,
        timestamp: Date.now()
      });
    } catch (error) {
      console.error(error);
    }
  };

  const handleStart = async () => {
    if (!activeDataset) return;
    
    setProcessing(true);
    addLog({
      agent: "SYSTEM",
      status: "Initializing MetaMind Multi-Agent Swarm...",
      timestamp: Date.now()
    });

    try {
      await fetch(`http://localhost:8000/run?dataset_path=${activeDataset}&instruction=${instruction}`, {
        method: 'POST'
      });
    } catch (error) {
      console.error(error);
      setProcessing(false);
    }
  };

  return (
    <div className="absolute top-6 right-6 w-80 cyber-panel flex flex-col z-30 overflow-hidden bg-black/60 shadow-[0_20px_50px_rgba(0,0,0,0.8)] border-white/5">
      <div className="p-6 border-b border-cyber-neon/20 bg-cyber-dark/80 relative overflow-hidden">
        <div className="absolute -right-4 -top-4 opacity-10">
           <Globe size={100} className="text-cyber-neon" />
        </div>
        <h1 className="text-3xl font-black italic tracking-tighter text-white flex items-center gap-2">
          METAMIND
        </h1>
        <div className="flex items-center gap-2 mt-1">
           <div className="w-1.5 h-1.5 bg-cyber-neon rounded-full animate-pulse shadow-[0_0_8px_#00f3ff]" />
           <p className="text-[9px] text-cyber-neon font-mono tracking-[0.4em] uppercase font-bold">Autonomous AI Labs v3.0</p>
        </div>
      </div>

      <div className="p-4 space-y-6">
        {/* Upload Section */}
        <div className="space-y-2">
          <label className="text-[10px] font-bold text-gray-500 uppercase flex items-center gap-2">
            <Database size={12} />
            Data Source
          </label>
          <div className="relative group">
            <input 
              type="file" 
              onChange={handleUpload}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            <div className={`p-4 border-2 border-dashed rounded-lg transition-all flex flex-col items-center justify-center gap-2 ${
              activeDataset ? 'border-accent/40 bg-accent/5' : 'border-gray-800'
            }`}>
              <Upload size={20} className={activeDataset ? 'text-accent' : 'text-gray-600'} />
              <span className="text-[10px] font-medium">
                {activeDataset ? activeDataset.split('/').pop() : 'Click to upload CSV'}
              </span>
            </div>
          </div>
        </div>

        {/* Instruction Section */}
        <div className="space-y-2">
          <label className="text-[10px] font-bold text-gray-500 uppercase flex items-center gap-2">
            <Settings size={12} />
            Objective
          </label>
          <textarea 
            className="w-full bg-cyber-dark/30 border border-gray-800 rounded-md p-3 text-xs text-white min-h-[80px] focus:border-cyber-neon transition-colors outline-none"
            value={instruction}
            onChange={(e) => setInstruction(e.target.value)}
            placeholder="Describe what you want to predict..."
          />
        </div>

        <button
          onClick={handleStart}
          disabled={!activeDataset || isProcessing}
          className={`w-full py-5 rounded-2xl font-black text-xs tracking-[0.2em] uppercase flex items-center justify-center gap-3 transition-all ${
            !activeDataset || isProcessing 
            ? 'bg-white/5 text-white/20 cursor-not-allowed border border-white/5' 
            : 'bg-cyber-neon text-black hover:shadow-[0_0_40px_rgba(0,243,255,0.6)] active:scale-95 group'
          }`}
        >
          {isProcessing ? (
             <div className="flex gap-1 items-center">
               <span className="w-1 h-3 bg-black animate-pulse" style={{ animationDelay: '0.1s' }} />
               <span className="w-1 h-3 bg-black animate-pulse" style={{ animationDelay: '0.2s' }} />
               <span className="w-1 h-3 bg-black animate-pulse" style={{ animationDelay: '0.2s' }} />
               SWARM_ACTIVE
             </div>
          ) : (
            <>
              <Play size={18} fill="black" className="group-hover:translate-x-1 transition-transform" />
              Engage Swarm Intelligence
            </>
          )}
        </button>
      </div>

      <div className="mt-auto p-4 bg-cyber-neon/5 border-t border-cyber-neon/10">
        <div className="flex items-center gap-2 text-cyber-neon">
          <Info size={12} />
          <span className="text-[9px] font-bold uppercase tracking-wider">System Status: Active</span>
        </div>
      </div>
    </div>
  );
};
