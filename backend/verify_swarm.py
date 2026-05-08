import asyncio
import os
import pandas as pd
from app.core.orchestrator import MetaMindOrchestrator
from dotenv import load_dotenv

load_dotenv()

async def mock_broadcast(data):
    print(f"[WS BROADCAST] {data['agent']}: {data['status']}")
    if 'data' in data:
        print(f"       DATA: {str(data['data'])[:200]}...")

async def verify():
    print("=== STARTING VIRTUAL VERIFICATION ===")
    orchestrator = MetaMindOrchestrator(on_status_update=mock_broadcast)
    
    dataset_path = "data/students_performance.csv"
    instruction = "Predict student performance"
    
    result = await orchestrator.run(dataset_path, instruction)
    
    print("\n=== VERIFICATION RESULTS ===")
    if result and result.get("status") == "success":
        print("✅ SWARM SUCCESS")
        print(f"📈 METRICS: {result.get('metrics')}")
        print(f"📝 EXPLANATION LENGTH: {len(result.get('explanation'))}")
    else:
        print("❌ SWARM FAILED")

if __name__ == "__main__":
    asyncio.run(verify())
