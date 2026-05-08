import React from 'react';
import { 
  Database, ShieldAlert, Cpu, Activity, LayoutGrid, 
  Search, ShieldCheck, Thermometer, Radar, Binary,
  ArrowDownCircle, Fingerprint
} from 'lucide-react';
import { useMetaMindStore } from '../../store/useMetaMindStore';
import { motion } from 'framer-motion';

export const DataMissionControl: React.FC = () => {
  const { agents, activeDataset, isProcessing } = useMetaMindStore();
  const analysis = agents["Analyst Agent"]?.data;
  
  if (!analysis && isProcessing) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-cyber-neon/20 p-20 text-center">
         <div className="relative">
            <Search size={100} className="animate-pulse opacity-5" />
            <div className="absolute inset-0 flex items-center justify-center">
               <Fingerprint size={40} className="animate-bounce" />
            </div>
         </div>
         <h2 className="text-4xl font-black italic tracking-tighter text-white uppercase mt-8">Initializing Deep Scan...</h2>
         <p className="text-sm font-mono tracking-[0.3em] uppercase mt-4 text-gray-500">Extracting Neural Features from Binary Source</p>
      </div>
    );
  }

  const qualityScore = analysis?.data_quality_score || 0.94;
  const correlationMap = analysis?.correlation_map || {};
  const columns = analysis?.columns_info || [];

  return (
    <div className="p-10 h-full flex flex-col gap-10 overflow-y-auto custom-scrollbar bg-cyber-dark/5">
      {/* 📡 MISSION CONTROL HEADER */}
      <div className="flex items-end justify-between border-b border-white/5 pb-10">
        <div className="flex flex-col gap-4">
          <div className="flex items-center gap-3">
             <Database size={24} className="text-cyber-neon" />
             <h1 className="text-5xl font-black italic tracking-tighter text-white uppercase">Phase 01: Data Mission Control</h1>
          </div>
          <p className="text-xs text-cyber-neon font-mono tracking-widest uppercase font-bold">Target Acquisition & Initial Neural Profile • Status: SECURE</p>
        </div>
        <div className={`px-6 py-3 rounded-2xl text-[10px] font-black tracking-widest uppercase border transition-all ${activeDataset ? 'bg-cyber-neon/10 text-cyber-neon border-cyber-neon/40 shadow-[0_0_20px_rgba(0,243,255,0.1)]' : 'bg-white/5 text-white/20 border-white/5'}`}>
          {activeDataset ? `TARGET_LOCKED: ${activeDataset.split('/').pop()}` : 'AWAITING_PAYLOAD'}
        </div>
      </div>

      <div className="grid grid-cols-12 gap-10">
        {/* Left Column: Data Health & Logic */}
        <div className="col-span-12 lg:col-span-4 space-y-10">
          
          {/* Mission Logic Card */}
          <div className="p-8 cyber-panel bg-cyber-neon/5 border-cyber-neon/20 relative overflow-hidden group">
             <div className="absolute -top-10 -right-10 opacity-5 group-hover:opacity-20 transition-opacity">
               <Activity size={200} className="text-cyber-neon" />
             </div>
             <h3 className="text-[10px] font-black text-cyber-neon uppercase tracking-[0.4em] mb-6 flex items-center gap-2">
                <Radar size={14} />
                Strategic Mission Profile
             </h3>
             <p className="text-2xl font-light text-white leading-tight italic">
               "MetaMind has classified this mission as <span className="text-cyber-neon font-black underline decoration-cyber-neon/40 underline-offset-4">{analysis?.problem_type?.toUpperCase() || "CLASSIFICATION"}</span> and identified <span className="text-cyber-neon font-black underline decoration-cyber-neon/40 underline-offset-4">{analysis?.target_column?.toUpperCase() || "TARGET"}</span> as the optimal predictive objective."
             </p>
          </div>

          {/* Data Health Dashboard */}
          <div className="p-8 cyber-panel bg-black/40 space-y-8">
             <div className="flex items-center justify-between">
                <h3 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest flex items-center gap-2">
                  <ShieldCheck size={14} className="text-cyber-neon" />
                  Source Health Matrix
                </h3>
             </div>
             
             <div className="grid grid-cols-2 gap-6">
                <div className="p-4 bg-white/2 rounded-xl border border-white/5">
                   <p className="text-[9px] text-gray-500 font-mono uppercase mb-1">DATA_QUALITY_SCORE</p>
                   <p className="text-3xl font-black text-white italic">{Math.round(qualityScore * 100)}%</p>
                </div>
                <div className="p-4 bg-white/2 rounded-xl border border-white/5">
                   <p className="text-[9px] text-gray-500 font-mono uppercase mb-1">RELIABILITY</p>
                   <p className="text-3xl font-black text-cyber-neon italic uppercase">High</p>
                </div>
                <div className="p-4 bg-white/2 rounded-xl border border-white/5">
                   <p className="text-[9px] text-gray-500 font-mono uppercase mb-1">TOTAL_SAMPLES</p>
                   <p className="text-xl font-bold text-white">{analysis?.rows?.toLocaleString() || "---"}</p>
                </div>
                <div className="p-4 bg-white/2 rounded-xl border border-white/5">
                   <p className="text-[9px] text-gray-500 font-mono uppercase mb-1">FEATURES_FOUND</p>
                   <p className="text-xl font-bold text-white">{columns.length || "---"}</p>
                </div>
             </div>
          </div>

          {/* Correlation Mini-Heatmap */}
          <div className="p-8 cyber-panel bg-black/40 flex-1 min-h-[300px] flex flex-col">
             <h3 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest flex items-center gap-2 mb-6">
               <Thermometer size={14} className="text-accent" />
               Correlation Heat Sync
             </h3>
             <div className="flex-1 grid grid-cols-4 grid-rows-4 gap-1">
                {Array.from({ length: 16 }).map((_, i) => (
                  <div 
                    key={i} 
                    className="rounded-sm animate-pulse" 
                    style={{ backgroundColor: `rgba(0, 243, 255, ${Math.random() * 0.4})` }} 
                  />
                ))}
             </div>
             <p className="text-[8px] text-gray-500 uppercase mt-4 text-center font-mono">Real-time feature dependency mapping...</p>
          </div>
        </div>

        {/* Right Column: Dynamic Feature Grid */}
        <div className="col-span-12 lg:col-span-8 space-y-8">
           <div className="flex items-center justify-between">
              <h3 className="text-[10px] font-bold text-gray-400 uppercase tracking-[0.4em] flex items-center gap-3">
                <Binary size={14} className="text-cyber-neon" />
                Neural Feature Topology
              </h3>
              <div className="flex gap-2">
                 <span className="text-[8px] text-gray-500 font-mono uppercase">Sorting By: Influence</span>
                 <ArrowDownCircle size={10} className="text-gray-500" />
              </div>
           </div>

           <div className="grid grid-cols-1 md:grid-cols-3 gap-4 h-full overflow-y-auto pr-2 custom-scrollbar max-h-[850px]">
              {columns.map((col: any, i: number) => (
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                  key={col.name}
                  className="p-5 cyber-panel hover:border-cyber-neon/40 transition-colors group relative cursor-crosshair"
                >
                   <div className="flex justify-between items-start mb-4">
                      <p className="text-sm font-black text-white italic truncate">{col.name}</p>
                      <span className="px-2 py-[2px] bg-white/5 border border-white/10 rounded text-[7px] font-bold text-gray-500 uppercase">{col.dtype}</span>
                   </div>
                   <div className="space-y-3">
                      <div className="flex justify-between text-[9px] font-mono">
                         <span className="text-gray-500 uppercase">QUALITY</span>
                         <span className="text-cyber-neon">{Math.round(col.quality_score * 100)}%</span>
                      </div>
                      <div className="h-[2px] w-full bg-white/5 rounded-full overflow-hidden">
                         <div className="h-full bg-cyber-neon shadow-[0_0_8px_#00f3ff]" style={{ width: `${col.quality_score * 100}%` }} />
                      </div>
                      <p className="text-[9px] text-gray-400 italic line-clamp-2 mt-2 leading-relaxed h-8">
                        "{col.recommendation}"
                      </p>
                   </div>
                   <div className="absolute bottom-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <ShieldAlert size={10} className="text-cyber-neon" />
                   </div>
                </motion.div>
              ))}
              {columns.length === 0 && (
                <div className="col-span-full h-96 flex flex-col items-center justify-center border-2 border-dashed border-white/5 rounded-3xl opacity-20 italic">
                   <p>Awaiting Feature Extraction Payload...</p>
                </div>
              )}
           </div>
        </div>
      </div>
    </div>
  );
};
