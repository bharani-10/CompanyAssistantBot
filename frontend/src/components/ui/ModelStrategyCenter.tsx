import React from 'react';
import { 
  Target, ShieldCheck, Scale, Cpu, Trophy, ArrowRight, AlertCircle, 
  ChevronRight, Fingerprint, Zap, Gauge, Flame
} from 'lucide-react';
import { useMetaMindStore } from '../../store/useMetaMindStore';
import { motion, AnimatePresence } from 'framer-motion';

export const ModelStrategyCenter: React.FC = () => {
  const { agents, isProcessing } = useMetaMindStore();
  const plan = agents["Architect Agent"]?.data;
  const critique = agents["Critic Agent"]?.data;
  
  if (!plan && isProcessing) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-white/20 p-20 text-center relative overflow-hidden">
         <div className="absolute inset-0 z-0 opacity-20">
            <Fingerprint size={400} className="text-cyber-neon animate-pulse" />
         </div>
         <div className="relative z-10 flex flex-col items-center">
            <Cpu size={80} className="mb-8 text-cyber-neon animate-spin" style={{ animationDuration: '4s' }} />
            <h2 className="text-4xl font-black italic uppercase tracking-tighter text-white">Strategizing Neural Architectures</h2>
            <p className="text-sm max-w-md mt-4 text-gray-500 font-mono tracking-widest uppercase">The Swarm is currently auditing candidate pipelines in the Strategic War Room...</p>
            <div className="mt-8 flex gap-2">
               {[1, 2, 3, 4, 5].map(i => (
                 <div key={i} className="w-1 h-3 bg-cyber-neon/40 animate-pulse" style={{ animationDelay: `${i * 0.1}s` }} />
               ))}
            </div>
         </div>
      </div>
    );
  }

  const models = plan?.models || [
    {
      name: "RandomForest Elite",
      rank: 1,
      accuracy_forecast: 0.94,
      explainability_score: 0.88,
      complexity: "Medium",
      latency: "Low",
      risk_level: "Minimal",
      strengths: ["Highly robust", "Non-linear capture", "Explainable"],
      weaknesses: ["Memory intensive for deep trees"],
      why_chosen: "Best overall balance for the detected regression target."
    },
    {
      name: "XGBoost Hyper",
      rank: 2,
      accuracy_forecast: 0.96,
      explainability_score: 0.65,
      complexity: "High",
      latency: "Medium",
      risk_level: "Elevated",
      strengths: ["Maximum performance", "Feature interaction"],
      weaknesses: ["High complexity", "Harder to explain to executives"],
      why_chosen: "Alternative for performance-critical scenarios.",
      why_rejected: "Complexity overhead exceeds marginal accuracy gain."
    }
  ];

  return (
    <div className="p-10 h-full flex flex-col gap-10 overflow-y-auto custom-scrollbar bg-cyber-dark/10">
      {/* 🛡️ STRATEGIC WAR ROOM HEADER */}
      <div className="flex items-end justify-between border-b border-white/5 pb-10">
        <div>
          <div className="flex items-center gap-3">
             <Flame className="text-accent" size={24} />
             <h1 className="text-5xl font-black italic tracking-tighter text-white uppercase">Phase 02: Strategic War Room</h1>
          </div>
          <p className="text-xs text-cyber-neon font-mono tracking-widest uppercase mt-4 font-bold">Algorithmic Competitive Selection • Swarm Consensus: ACTIVE</p>
        </div>
        <div className="flex flex-col items-end gap-2">
           <span className="text-[10px] font-mono text-gray-500">CONSENSUS_LEVEL</span>
           <div className="flex gap-1">
              {[1, 2, 3, 4].map(i => <div key={i} className="w-6 h-1 bg-cyber-neon shadow-[0_0_8px_#00f3ff]" />)}
              <div className="w-6 h-1 bg-white/10" />
           </div>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-10">
        {/* Model Dossiers */}
        <div className="col-span-12 lg:col-span-8 space-y-8">
           <h3 className="text-[10px] font-bold text-gray-400 uppercase tracking-[0.4em] flex items-center gap-3">
             <Target size={14} className="text-cyber-neon" fill="currentColor" />
             Strategic Path Comparison
           </h3>
           
           <div className="grid grid-cols-1 gap-6">
              {models.map((model: any, idx: number) => (
                <motion.div 
                  initial={{ opacity: 0, x: -30 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.15 }}
                  key={model.name}
                  className={`p-8 cyber-panel relative group transition-all duration-500 ${idx === 0 ? 'border-cyber-neon bg-cyber-neon/5 shadow-[0_0_40px_rgba(0,243,255,0.1)]' : 'border-white/5 bg-white/2'}`}
                >
                   {idx === 0 && (
                      <div className="absolute -top-3 left-8 px-4 py-1 bg-cyber-neon text-black text-[8px] font-black italic uppercase tracking-widest rounded-full z-10">
                         PRIMARY_STRATEGY
                      </div>
                   )}

                   <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                     <div className="flex items-center gap-6">
                        <div className={`p-5 rounded-2xl ${idx === 0 ? 'bg-cyber-neon/20 text-cyber-neon' : 'bg-white/5 text-white/40'}`}>
                           {idx === 0 ? <Trophy size={32} /> : <Zap size={32} />}
                        </div>
                        <div>
                           <h4 className="text-2xl font-black text-white italic uppercase">{model.name}</h4>
                           <div className="flex gap-3 mt-2">
                              <span className="text-[9px] font-mono text-gray-500 underline decoration-white/10 underline-offset-4">RANK: 0{model.rank}</span>
                              <span className="text-[9px] font-mono text-gray-500 underline decoration-white/10 underline-offset-4">RISK: {model.risk_level.toUpperCase()}</span>
                           </div>
                        </div>
                     </div>
                     
                     <div className="flex gap-6 items-center">
                        <div className="text-right">
                           <p className="text-[8px] text-gray-500 font-mono uppercase mb-1">ACCURACY_EST</p>
                           <p className={`text-2xl font-black ${idx === 0 ? 'text-cyber-neon' : 'text-white'}`}>{Math.round(model.accuracy_forecast * 100)}%</p>
                        </div>
                        <div className="w-[1px] h-10 bg-white/5 hidden md:block" />
                        <div className="text-right">
                           <p className="text-[8px] text-gray-500 font-mono uppercase mb-1">EXPLAIN_INDEX</p>
                           <p className="text-2xl font-black text-white">{Math.round(model.explainability_score * 100)}</p>
                        </div>
                     </div>
                   </div>

                   <div className="mt-10 grid grid-cols-1 md:grid-cols-2 gap-10">
                      <div className="space-y-4">
                         <p className="text-[9px] font-bold text-cyber-neon uppercase tracking-widest">Strengths</p>
                         <ul className="space-y-3">
                            {model.strengths.map((s: string) => (
                              <li key={s} className="flex items-center gap-2 text-[11px] text-gray-400">
                                 <ChevronRight size={12} className="text-cyber-neon" />
                                 {s}
                              </li>
                            ))}
                         </ul>
                      </div>
                      <div className="space-y-4">
                         <p className="text-[9px] font-bold text-accent uppercase tracking-widest">Selection Rationale</p>
                         <p className="text-[11px] leading-relaxed text-white/60 italic border-l-2 border-white/10 pl-4 py-2">
                           "{idx === 0 ? model.why_chosen : model.why_rejected}"
                         </p>
                      </div>
                   </div>
                </motion.div>
              ))}
           </div>
        </div>

        {/* The Strategizer Feedback */}
        <div className="col-span-12 lg:col-span-4 space-y-8">
           <h3 className="text-[10px] font-bold text-gray-400 uppercase tracking-[0.4em] flex items-center gap-3">
             <Scale size={14} className="text-accent" />
             Swarm Conflict Resolution
           </h3>
           
           <div className="p-8 cyber-panel bg-cyber-dark/40 border-accent/20 relative overflow-hidden group min-h-[600px]">
              <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-20 transition-opacity">
                 <ShieldCheck size={120} className="text-accent" />
              </div>
              
              <div className="space-y-8 relative z-10">
                 <div className="space-y-3">
                    <p className="text-[10px] text-accent font-black tracking-widest uppercase">Critic Intelligence Audit</p>
                    <div className="text-sm italic text-white leading-relaxed bg-black/60 p-6 rounded-2xl border border-white/5 shadow-inner">
                       "{critique?.reason || "Auditing the Architect's proposed strategy for data leakage, computational overhead, and corporate interpretability standards..."}"
                    </div>
                 </div>

                 <div className="space-y-6">
                    <p className="text-[10px] text-gray-500 font-mono tracking-widest uppercase">Calibration Matrix</p>
                    <div className="space-y-4">
                       {[
                         { label: 'Latency Threshold', val: 92 },
                         { label: 'Interpretability Bias', val: 78 },
                         { label: 'Overfitting Risk', val: 15 },
                       ].map(stat => (
                         <div key={stat.label} className="space-y-2">
                            <div className="flex justify-between text-[9px] font-mono text-gray-400">
                               <span>{stat.label.toUpperCase()}</span>
                               <span>{stat.val}%</span>
                            </div>
                            <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                               <motion.div 
                                 initial={{ width: 0 }}
                                 animate={{ width: `${stat.val}%` }}
                                 className={`h-full ${stat.val > 80 ? 'bg-cyber-neon' : 'bg-accent'}`} 
                               />
                            </div>
                         </div>
                       ))}
                    </div>
                 </div>

                 <div className="pt-8 border-t border-white/5 space-y-4">
                    <div className="flex items-center gap-3 text-[11px] text-white/50">
                       <AlertCircle size={14} className="text-cyber-neon" />
                       Strategy Alignment: PERFECT
                    </div>
                    <button className="w-full py-4 bg-white/5 border border-white/10 rounded-xl text-[10px] font-bold text-white uppercase tracking-widest hover:bg-white/10 transition-colors flex items-center justify-center gap-3">
                       Expert Decision Matrix
                       <ArrowRight size={14} />
                    </button>
                 </div>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
};
