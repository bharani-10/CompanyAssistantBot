import asyncio
import os
import pandas as pd
import json
from app.core.orchestrator import MetaMindOrchestrator
from dotenv import load_dotenv

load_dotenv()

async def mock_broadcast(data):
    print(f"[WS BROADCAST] {data['agent']}: {data['status']}")

async def verify():
    print("=== STARTING VIRTUAL VERIFICATION ===")
    orchestrator = MetaMindOrchestrator(on_status_update=mock_broadcast)
    
    dataset_path = "data/students_performance.csv"
    instruction = "Predict student performance"
    
    result = await orchestrator.run(dataset_path, instruction)
    
    print("\n=== VERIFICATION RESULTS ===")
    if result and result.get("status") == "success":
        print("RESULT: SUCCESS")
        print(f"METRICS: {json.dumps(result.get('metrics'))}")
        # print(f"EXPLANATION: {result.get('explanation')[:200]}...")
    else:
        print("RESULT: FAILED")

if __name__ == "__main__":
    asyncio.run(verify())
