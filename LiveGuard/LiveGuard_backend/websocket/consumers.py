import os
import uuid
import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer

class FrameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """WebSocket 연결 처리"""
        try:
            await self.accept()
            print("WebSocket connected.")
        except Exception as e:
            print(f"Error during WebSocket connect: {e}")
            await self.close()

    async def disconnect(self, close_code):
        """WebSocket 연결 종료 처리"""
        print(f"WebSocket disconnected: {close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        """WebSocket 데이터 수신 및 처리"""
        try:
            if text_data:
                # 텍스트 데이터 처리 (디버깅 용도)
                print(f"Received text data: {text_data}")
                await self.send(text_data=json.dumps({
                    'message': 'Hello, Client!',
                }))

            if bytes_data:
                # 저장 디렉터리 설정
                save_dir = "/home/dackeld17/LiveGuard/LiveGuard_backend/websocket/frame"
                os.makedirs(save_dir, exist_ok=True)  # 디렉터리 생성

                # 고유 파일 이름 생성
                unique_filename = f"frame_{uuid.uuid4().hex}.jpg"
                file_path = os.path.join(save_dir, unique_filename)

                # 파일 저장
                with open(file_path, "wb") as f:
                    f.write(bytes_data)
                print(f"Frame saved at: {file_path}")

                # Base64로 인코딩하여 브라우저로 전송
                encoded_frame = base64.b64encode(bytes_data).decode('utf-8')
                await self.send(text_data=encoded_frame)
                print("Frame sent to browser.")

        except Exception as e:
            print(f"Error during WebSocket receive: {e}")
            await self.close()

