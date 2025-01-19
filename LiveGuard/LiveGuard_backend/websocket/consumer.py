import os
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer

class WebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            await self.accept()
            print("WebSocket connected.")
        except Exception as e:
            print(f"Error during WebSocket connect: {e}")
            await self.close()

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected: {close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data:
                print(f"Received text data: {text_data}")
                await self.send(text_data=json.dumps({
                    'message': 'Hello, Client!',
                }))

            if bytes_data:
                # 저장 디렉터리 설정
                save_dir = "/home/dackeld17/LiveGuard/LiveGuard_backend/websocket/frame"
                os.makedirs(save_dir, exist_ok=True)  # 디렉터리 생성

                # 고유 파일 이름 생성 (UUID 사용)
                unique_filename = f"frame_{uuid.uuid4().hex}.jpg"
                file_path = os.path.join(save_dir, unique_filename)

                # 파일 저장
                with open(file_path, "wb") as f:
                    f.write(bytes_data)
                print(f"Frame saved at: {file_path}")
            else:
                print("No bytes_data received.")
        except Exception as e:
            print(f"Error during WebSocket receive: {e}")
            await self.close()

class FrameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # WebSocket 연결 수락
        await self.accept()

    async def disconnect(self, close_code):
        # WebSocket 연결 종료 처리
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            print(f"Received bytes_data of size: {len(bytes_data)}")  # 로그 추가
            encoded_frame = base64.b64encode(bytes_data).decode('utf-8')
            await self.send(text_data=encoded_frame)

