import cv2
import asyncio
import websockets
import base64

async def send_webcam_feed(websocket, path):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Encode the frame in JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = base64.b64encode(buffer).decode('utf-8')

        # Send the frame data to the client
        await websocket.send(frame_data)

        # Limit the frame rate
        await asyncio.sleep(0.1)

    cap.release()

start_server = websockets.serve(send_webcam_feed, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
