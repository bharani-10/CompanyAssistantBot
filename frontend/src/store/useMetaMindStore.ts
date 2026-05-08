import { create } from 'zustand';

export interface AgentStatus {
  agent: string;
  status: string;
  data?: any;
  timestamp: number;
}

export type MetaMindView = 'MISSION' | 'STRATEGY' | 'THEATER' | 'COMMAND';

interface MetaMindState {
  agents: Record<string, { status: string; lastUpdate: number; data: any }>;
  logs: AgentStatus[];
  isProcessing: boolean;
  activeDataset: string | null;
  currentView: MetaMindView;
  missionStats: { duration: string; dataPoints: number };
  
  // Actions
  updateAgent: (agent: string, status: string, data?: any) => void;
  addLog: (log: AgentStatus) => void;
  setProcessing: (bool: boolean) => void;
  setDataset: (path: string | null) => void;
  setView: (view: MetaMindView) => void;
  setMissionStats: (stats: { duration: string; dataPoints: number }) => void;
  reset: () => void;
}

export const useMetaMindStore = create<MetaMindState>((set) => ({
  agents: {
    "Analyst Agent": { status: "IDLE", lastUpdate: 0, data: null },
    "Architect Agent": { status: "IDLE", lastUpdate: 0, data: null },
    "Engineer Agent": { status: "IDLE", lastUpdate: 0, data: null },
    "Executor Agent": { status: "IDLE", lastUpdate: 0, data: null },
    "Evaluator Agent": { status: "IDLE", lastUpdate: 0, data: null },
    "Critic Agent": { status: "IDLE", lastUpdate: 0, data: null },
    "Explainer Agent": { status: "IDLE", lastUpdate: 0, data: null },
  },
  logs: [],
  isProcessing: false,
  activeDataset: null,
  currentView: 'MISSION',
  missionStats: { duration: '00:00:00', dataPoints: 0 },

  setMissionStats: (stats) => set({ missionStats: stats }),

  updateAgent: (agent, status, data = null) => set((state) => ({
    agents: {
      ...state.agents,
      [agent]: { status, lastUpdate: Date.now(), data: data || state.agents[agent]?.data }
    }
  })),

  addLog: (log) => set((state) => ({
    logs: [log, ...state.logs].slice(0, 50) // Keep last 50
  })),

  setProcessing: (bool) => set({ isProcessing: bool }),
  
  setDataset: (path) => set({ activeDataset: path }),

  setView: (view) => set({ currentView: view }),

  reset: () => set({
    logs: [],
    isProcessing: false,
    currentView: 'MISSION',
    agents: {
      "Analyst Agent": { status: "IDLE", lastUpdate: 0, data: null },
      "Architect Agent": { status: "IDLE", lastUpdate: 0, data: null },
      "Engineer Agent": { status: "IDLE", lastUpdate: 0, data: null },
      "Executor Agent": { status: "IDLE", lastUpdate: 0, data: null },
      "Evaluator Agent": { status: "IDLE", lastUpdate: 0, data: null },
      "Critic Agent": { status: "IDLE", lastUpdate: 0, data: null },
      "Explainer Agent": { status: "IDLE", lastUpdate: 0, data: null },
    }
  })
}));
