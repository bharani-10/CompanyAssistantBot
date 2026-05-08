import React, { useEffect, useRef } from 'react';
import { useMetaMindStore } from '../../store/useMetaMindStore';
import { Terminal as TerminalIcon, Cpu, AlertCircle } from 'lucide-react';

export const Terminal: React.FC = () => {
  const logs = useMetaMindStore(state => state.logs);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="absolute bottom-6 right-6 w-96 h-48 cyber-panel flex flex-col overflow-hidden z-20">
      <div className="flex items-center justify-between px-4 py-2 border-b border-cyber-neon/20 bg-cyber-dark">
        <div className="flex items-center gap-2">
          <TerminalIcon size={14} className="text-cyber-neon" />
          <span className="text-[10px] font-bold uppercase tracking-wider text-white">System Feed</span>
        </div>
        <div className="flex gap-1">
          <div className="w-2 h-2 rounded-full bg-red-500/50" />
          <div className="w-2 h-2 rounded-full bg-yellow-500/50" />
          <div className="w-2 h-2 rounded-full bg-green-500/50" />
        </div>
      </div>
      
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 font-mono text-[11px] space-y-2 custom-scrollbar"
      >
        {logs.length === 0 && (
          <div className="text-gray-600 italic">Waiting for agents to initialize...</div>
        )}
        {logs.map((log, i) => (
          <div key={i} className="animate-in fade-in slide-in-from-left-2 duration-300">
            <div className="flex items-start gap-2">
              <span className="text-gray-500 flex-shrink-0">[{new Date(log.timestamp).toLocaleTimeString([], { hour12: false })}]</span>
              <span className="text-cyber-neon font-bold uppercase shrink-0">{log.agent}:</span>
              <span className="text-white/90 break-words">{log.status}</span>
            </div>
            {log.data && (
              <pre className="mt-1 ml-4 text-[9px] text-accent/70 bg-accent/5 p-1 rounded overflow-x-auto">
                {JSON.stringify(log.data, null, 2)}
              </pre>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
