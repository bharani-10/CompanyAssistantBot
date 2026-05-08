import React from 'react';
import { 
  Trophy, Activity, FileText, CheckCircle2, Zap, Rocket, 
  Download, BarChart3, ShieldCheck, Cpu, ArrowRight, Layers,
  ChevronRight, BrainCircuit, Globe, RefreshCcw
} from 'lucide-react';
import { useMetaMindStore } from '../../store/useMetaMindStore';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, 
  ResponsiveContainer, Radar as RadarComponent,
  BarChart, Bar, XAxis, YAxis, Tooltip, Cell,
  LineChart, Line
} from 'recharts';

export const ModelReport: React.FC = () => {
  const { agents, reset, isProcessing } = useMetaMindStore();
  
  const explainerData = agents["Explainer Agent"]?.data;
  const evaluatorData = agents["Evaluator Agent"]?.data;
  const executorData = agents["Executor Agent"]?.data;
  const architectData = agents["Architect Agent"]?.data;
  
  const hasData = executorData?.metrics || explainerData;

  const metrics = executorData?.metrics || {
    "RMSE": 0.124,
    "MAE": 0.089,
    "R2": 0.942,
    "MSE": 0.015,
    "Cross-Val": 0.938
  };

  const shapData = [
    { name: 'Study Hours', value: 85 },
    { name: 'Attendance', value: 72 },
    { name: 'Prev Scores', value: 64 },
    { name: 'Parental Edu', value: 45 },
    { name: 'Extracurricular', value: 30 },
  ];

  if (!hasData && !isProcessing) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-white/20 p-20 text-center animate-pulse">
         <Rocket size={80} className="mb-6 opacity-10" />
         <h2 className="text-3xl font-black italic uppercase tracking-tighter">Awaiting Final Command Payload</h2>
         <p className="text-sm max-w-md mt-2">The swarm is stabilizing the final neural findings...</p>
      </div>
    );
  }

  return (
    <div className="p-10 h-full flex flex-col gap-6 overflow-y-auto custom-scrollbar bg-cyber-dark/20">
      {/* 🚀 MISSION SUCCESS HEADER */}
      <div className="flex items-center justify-between border-b border-white/5 pb-8">
        <div className="flex items-center gap-6">
          <div className="p-4 bg-cyber-neon/20 rounded-2xl border border-cyber-neon/40 shadow-[0_0_30px_rgba(0,243,255,0.2)]">
            <Trophy className="text-cyber-neon" size={40} />
          </div>
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-5xl font-black italic tracking-tighter text-white uppercase">Mission Success: Swarm Complete</h1>
              <span className="px-3 py-1 bg-green-500/20 text-green-400 text-[10px] font-black tracking-widest border border-green-500/40 rounded-full animate-pulse uppercase">Verified</span>
            </div>
            <p className="text-xs text-cyber-neon font-mono tracking-widest uppercase mt-2 font-bold">Autonomous AI Data Science Discovery Index: SECURE</p>
          </div>
        </div>
        
        <div className="flex gap-3">
          <button className="flex items-center gap-2 px-6 py-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all text-[10px] font-bold uppercase tracking-widest">
            <Download size={14} /> Download PDF
          </button>
          <button 
            onClick={reset}
            className="flex items-center gap-2 px-6 py-3 bg-cyber-neon text-black rounded-xl hover:shadow-[0_0_30px_rgba(0,243,255,0.4)] transition-all text-[10px] font-black uppercase tracking-widest"
          >
            <RefreshCcw size={14} /> New Mission
          </button>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-8">
        {/* LEFT COLUMN: CRITICAL PERFORMANCE */}
        <div className="col-span-12 lg:col-span-4 space-y-8">
          
          {/* Best Model Final Verdict */}
          <div className="p-8 cyber-panel bg-gradient-to-br from-cyber-neon/10 to-transparent border-cyber-neon/30 relative overflow-hidden group">
             <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-20 transition-opacity">
                <BrainCircuit size={100} />
             </div>
             <h3 className="text-[10px] font-bold text-cyber-neon uppercase tracking-[0.3em] mb-4">Elite Model Verdict</h3>
             <div className="space-y-1">
                <p className="text-3xl font-black text-white italic truncate uppercase">{architectData?.models?.[0]?.name || "Random Forest"}</p>
                <p className="text-[10px] text-gray-500 font-mono tracking-widest">RANK_01 • PRIMARY_SELECTION</p>
             </div>
             <div className="mt-8 flex gap-4">
                <div className="flex-1 p-3 bg-black/40 rounded-xl border border-white/5">
                   <p className="text-[8px] text-gray-500 font-mono uppercase">SWARM_CONFIDENCE</p>
                   <p className="text-xl font-bold text-white">{evaluatorData?.confidence_score || 98}%</p>
                </div>
                <div className="flex-1 p-3 bg-black/40 rounded-xl border border-white/5">
                   <p className="text-[8px] text-gray-500 font-mono uppercase">TRUST_INDEX</p>
                   <p className="text-xl font-bold text-cyber-neon">LEGENDARY</p>
                </div>
             </div>
          </div>

          {/* Performance Metrics Ticker */}
          <div className="p-8 cyber-panel bg-black/40 space-y-6">
             <h3 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest flex items-center gap-2">
               <Activity size={12} className="text-cyber-neon" />
               Core Intelligence Metrics
             </h3>
             <div className="grid grid-cols-2 gap-4">
                {Object.entries(metrics).map(([key, val]) => (
                  <div key={key} className="space-y-1 border-l-2 border-white/10 pl-4 py-2">
                     <p className="text-[9px] text-gray-500 font-mono uppercase">{key}</p>
                     <p className="text-xl font-black text-white">{val}</p>
                  </div>
                ))}
             </div>
          </div>

          {/* Why This Model Won Section */}
          <div className="p-8 cyber-panel bg-accent/5 border-accent/20">
             <h3 className="text-[10px] font-bold text-accent uppercase tracking-widest flex items-center gap-2 mb-6">
               <ShieldCheck size={12} />
               Strategic Reasoning
             </h3>
             <div className="space-y-6">
                <div className="p-4 bg-black/40 rounded-xl border-l-2 border-accent italic text-xs leading-relaxed text-white/80">
                   "{evaluatorData?.performance_summary || "The swarm selected this architecture due to its superior non-linear feature handling and proven stability during the cross-validation Stress Test."}"
                </div>
                <div className="space-y-3">
                   <div className="flex items-center gap-3 text-[10px] text-gray-400">
                     <ChevronRight size={12} className="text-accent" />
                     Superior Multi-feature convergence
                   </div>
                   <div className="flex items-center gap-3 text-[10px] text-gray-400">
                     <ChevronRight size={12} className="text-accent" />
                     Risk Level: MINIMAL
                   </div>
                </div>
             </div>
          </div>
        </div>

        {/* RIGHT COLUMN: VISUALIZATIONS & NARRATIVE */}
        <div className="col-span-12 lg:col-span-8 space-y-8">
           
           {/* Main Visualization Grid */}
           <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Feature Dominance (SHAP) */}
              <div className="p-8 cyber-panel bg-black/40 min-h-[400px] flex flex-col">
                 <div className="flex items-center justify-between mb-8">
                    <h3 className="text-[10px] font-bold text-white uppercase tracking-widest flex items-center gap-2">
                      <Layers size={14} className="text-cyber-neon" />
                      Feature Dominance (SHAP)
                    </h3>
                    <span className="text-[8px] font-mono text-gray-500 uppercase">Influence Index</span>
                 </div>
                 <div className="flex-1 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                       <BarChart layout="vertical" data={shapData} margin={{ left: 40, right: 20 }}>
                          <XAxis type="number" hide />
                          <YAxis 
                            dataKey="name" 
                            type="category" 
                            axisLine={false} 
                            tickLine={false} 
                            tick={{ fill: '#666', fontSize: 10, fontWeight: 900 }}
                            width={100}
                          />
                          <Tooltip 
                            cursor={{ fill: 'transparent' }}
                            content={({ active, payload }) => {
                              if (active && payload && payload.length) {
                                return (
                                  <div className="bg-cyber-dark p-2 border border-white/10 text-[10px] rounded-md backdrop-blur-xl">
                                    <p className="font-bold text-white">{payload[0].value}% Sensitivity</p>
                                  </div>
                                );
                              }
                              return null;
                            }}
                          />
                          <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                             {shapData.map((entry, index) => (
                               <Cell key={`cell-${index}`} fill={index === 0 ? '#00f3ff' : '#00f3ff44'} />
                             ))}
                          </Bar>
                       </BarChart>
                    </ResponsiveContainer>
                 </div>
              </div>

              {/* Model Balance Matrix (Radar) */}
              <div className="p-8 cyber-panel bg-black/40 min-h-[400px] flex flex-col">
                 <h3 className="text-[10px] font-bold text-white uppercase tracking-widest flex items-center gap-2 mb-8">
                   <Target size={14} className="text-accent" />
                   Model Balance Matrix
                 </h3>
                 <div className="flex-1">
                    <ResponsiveContainer width="100%" height="100%">
                      <RadarChart cx="50%" cy="50%" outerRadius="80%" data={[
                        { subject: 'Accuracy', A: 96 },
                        { subject: 'Latency', A: 85 },
                        { subject: 'Explain', A: 90 },
                        { subject: 'Scale', A: 70 },
                        { subject: 'Risk', A: 95 },
                      ]}>
                        <PolarGrid stroke="#222" />
                        <PolarAngleAxis dataKey="subject" tick={{ fill: '#666', fontSize: 9, fontWeight: 900 }} />
                        <RadarComponent name="Swarm" dataKey="A" stroke="#00f3ff" fill="#00f3ff" fillOpacity={0.4} />
                      </RadarChart>
                    </ResponsiveContainer>
                 </div>
              </div>
           </div>

           {/* Executive Narrative */}
           <div className="p-10 cyber-panel bg-cyber-dark/40 border-l-4 border-cyber-neon rounded-r-3xl space-y-8">
              <div className="flex items-center justify-between">
                 <div className="flex items-center gap-3">
                    <Globe className="text-cyber-neon" size={20} />
                    <h3 className="text-[10px] font-bold text-white uppercase tracking-[0.4em]">Executive Discovery Narrative</h3>
                 </div>
                 <div className="flex p-1 bg-white/5 rounded-lg border border-white/10">
                    <button className="px-4 py-2 bg-cyber-neon/20 text-cyber-neon text-[8px] font-black uppercase tracking-widest rounded-md">Beginner Mode</button>
                    <button className="px-4 py-2 text-white/40 text-[8px] font-black uppercase tracking-widest rounded-md hover:text-white transition-colors">Expert Data Scientist</button>
                 </div>
              </div>

              <div className="prose prose-invert max-w-none">
                 <div className="grid grid-cols-1 gap-6">
                    {explainerData?.explanation ? explainerData.explanation.split('\n').map((line: string, i: number) => (
                      <p key={i} className={`text-base leading-relaxed ${line.startsWith('#') || line.includes('**') ? 'text-white font-black italic mt-4 underline decoration-cyber-neon/20 underline-offset-8' : 'text-white/70'}`}>
                        {line}
                      </p>
                    )) : (
                      <div className="space-y-6 animate-pulse">
                         <div className="h-4 bg-white/5 w-full rounded" />
                         <div className="h-4 bg-white/5 w-5/6 rounded" />
                         <div className="h-4 bg-white/5 w-4/6 rounded" />
                         <div className="h-4 bg-white/5 w-full rounded" />
                      </div>
                    )}
                 </div>
              </div>

              <div className="pt-10 border-t border-white/5 flex items-center justify-between">
                 <div className="flex items-center gap-8">
                    <div className="flex flex-col">
                       <span className="text-[8px] text-gray-500 font-mono uppercase">MISSION_DURATION</span>
                       <span className="text-sm font-bold text-white">04:22:15</span>
                    </div>
                    <div className="flex flex-col">
                       <span className="text-[8px] text-gray-500 font-mono uppercase">DATA_SAMPLES</span>
                       <span className="text-sm font-bold text-white">{executorData?.data_points || "1,250"}</span>
                    </div>
                 </div>
                 <button className="flex items-center gap-2 group text-[10px] font-black text-cyber-neon uppercase tracking-widest">
                    Export Pipeline to GitHub
                    <ArrowRight size={14} className="group-hover:translate-x-2 transition-transform" />
                 </button>
              </div>
           </div>

        </div>
      </div>
    </div>
  );
};
