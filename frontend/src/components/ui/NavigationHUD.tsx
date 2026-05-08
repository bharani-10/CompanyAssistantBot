import React from 'react';
import { useMetaMindStore, MetaMindView } from '../../store/useMetaMindStore';
import { Database, Target, Cpu, Activity, Trophy } from 'lucide-react';

export const NavigationHUD: React.FC = () => {
  const { currentView, setView, isProcessing } = useMetaMindStore();

  const navItems: { id: MetaMindView; label: string; icon: any; page: string }[] = [
    { id: 'MISSION', label: 'DATA SCAN', icon: Database, page: '01' },
    { id: 'STRATEGY', label: 'STRATEGY', icon: Target, page: '02' },
    { id: 'THEATER', label: 'PROCESS', icon: Cpu, page: '03' },
    { id: 'COMMAND', label: 'COMMAND', icon: Trophy, page: '04' },
  ];

  return (
    <div className="fixed bottom-10 left-1/2 -translate-x-1/2 z-[100] flex items-center p-2 bg-black/60 backdrop-blur-2xl border border-white/10 rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.5)]">
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = currentView === item.id;
        
        return (
          <button
            key={item.id}
            onClick={() => setView(item.id)}
            className={`group relative px-6 py-3 flex flex-col items-center transition-all duration-500 rounded-xl ${
              isActive 
                ? 'bg-cyber-neon/10 text-cyber-neon scale-110' 
                : 'text-white/40 hover:text-white/80'
            }`}
          >
            {isActive && (
              <div className="absolute -top-1 left-1/2 -translate-x-1/2 w-8 h-[2px] bg-cyber-neon shadow-[0_0_10px_#00f3ff]" />
            )}
            <Icon size={18} className={isActive ? 'animate-pulse' : ''} />
            <span className="text-[8px] font-black tracking-[0.2em] mt-1.5 uppercase drop-shadow-md">
              {item.label}
            </span>
            <span className={`absolute -right-1 top-2 text-[6px] font-mono opacity-20 ${isActive ? 'opacity-100' : ''}`}>
              {item.page}
            </span>
          </button>
        );
      })}
      
      {isProcessing && (
        <div className="mx-4 h-8 w-[1px] bg-white/10" />
      )}
      
      {isProcessing && (
        <div className="pr-6 flex items-center gap-3">
          <div className="flex gap-1">
            {[1, 2, 3].map((i) => (
              <div 
                key={i} 
                className="w-1 h-3 bg-cyber-neon/40 animate-pulse" 
                style={{ animationDelay: `${i * 0.1}s` }} 
              />
            ))}
          </div>
          <span className="text-[8px] font-black text-cyber-neon uppercase tracking-widest animate-pulse">
            Processing Swarm...
          </span>
        </div>
      )}
    </div>
  );
};
