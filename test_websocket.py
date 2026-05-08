#!/usr/bin/env python3
"""
Test WebSocket connection to verify real-time communication
"""
import asyncio
import websockets
import json

async def test_websocket():
    try:
        print("🔌 Testing WebSocket connection...")
        uri = "ws://localhost:8000/ws"
        
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connected successfully!")
            
            # Send a test message
            await websocket.send("test message")
            print("📤 Sent test message")
            
            # Wait for any incoming messages for 5 seconds
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"📥 Received: {message}")
            except asyncio.TimeoutError:
                print("⏰ No messages received (timeout)")
            
            print("✅ WebSocket test completed")
            
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())