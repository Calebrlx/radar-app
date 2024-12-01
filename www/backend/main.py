import serial
import asyncio
import json
import time
import websockets

# Configuration for the radar module
RADAR_PORT = '/dev/ttyTHS1'
RADAR_BAUDRATE = 256000

# WebSocket configuration
WEBSOCKET_HOST = "localhost"
WEBSOCKET_PORT = 8000

def decode_packet(raw_data):
    try:
        if len(raw_data) < 10:
            return {"Angle": None, "Distance (mm)": None, "Speed (mm/s)": None}

        angle = int.from_bytes(raw_data[4:6], byteorder='little', signed=False)
        distance = int.from_bytes(raw_data[6:8], byteorder='little', signed=False)
        speed = int.from_bytes(raw_data[8:10], byteorder='little', signed=False)

        return {"Angle": angle, "Distance (mm)": distance, "Speed (mm/s)": speed}
    except Exception as e:
        print(f"Error decoding packet: {e}")
        return {"Angle": None, "Distance (mm)": None, "Speed (mm/s)": None}

async def radar_data_listener(websocket):
    try:
        with serial.Serial(RADAR_PORT, RADAR_BAUDRATE, timeout=1) as ser:
            while True:
                if ser.in_waiting:
                    raw_data = ser.read(ser.in_waiting)
                    decoded_data = decode_packet(raw_data)
                    await websocket.send(json.dumps(decoded_data))
                await asyncio.sleep(0.1)
    except Exception as e:
        print(f"Error: {e}")

async def main():
    async with websockets.serve(radar_data_listener, WEBSOCKET_HOST, WEBSOCKET_PORT):
        print(f"WebSocket server running at ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
