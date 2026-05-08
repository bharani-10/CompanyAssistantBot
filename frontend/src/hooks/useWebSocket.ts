import { useEffect, useRef } from 'react';
import { useMetaMindStore, AgentStatus } from '../store/useMetaMindStore';

export const useWebSocket = (url: string) => {
  const ws = useRef<WebSocket | null>(null);
  const { updateAgent, addLog, setProcessing, setView, setMissionStats } = useMetaMindStore();

  useEffect(() => {
    let missionStartTime = 0;
    const connect = () => {
      ws.current = new WebSocket(url);

      ws.current.onopen = () => {
        console.log('Connected to MetaMind WebSocket');
        missionStartTime = Date.now();
      };

      ws.current.onmessage = (event) => {
        const message = JSON.parse(event.data);
        const { agent, status, data } = message;

        updateAgent(agent, status, data);
        addLog({ agent, status, data, timestamp: Date.now() });

        // Phase Progression Logic
        if (agent === "Analyst Agent" && status === "Analysis complete") {
          setView('STRATEGY');
        } else if (agent === "Architect Agent" && status === "Consensus reached. Architecture locked.") {
          setView('THEATER');
        } else if (status === "All tasks complete") {
          const duration = new Date(Date.now() - missionStartTime).toISOString().substr(11, 8);
          setMissionStats({ duration, dataPoints: data?.data_points || 1250 });
          setView('COMMAND');
        }

        if (status === "PROCESS_FINISHED" || agent === "SYSTEM ERROR") {
          setProcessing(false);
        }
      };

      ws.current.onclose = () => {
        console.log('WebSocket disconnected. Retrying in 3s...');
        setTimeout(connect, 3000);
      };

      ws.current.onerror = (err) => {
        console.error('WebSocket Error:', err);
        ws.current?.close();
      };
    };

    connect();

    return () => {
      ws.current?.close();
    };
  }, [url]);

  return ws.current;
};
