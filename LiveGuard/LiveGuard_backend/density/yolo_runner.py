import cv2
import time
from ultralytics import YOLO
from dataclasses import dataclass

@dataclass
class DetectionResult:
    boxes: list
    scores: list
    num_people: int
    density: float
    stage: str
    fps: float

class YOLOPeopleDetector:
    def __init__(self, model_path: str, confidence_threshold: float = 0.5):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

    def process_frame(self, frame):
        start_time = time.time()
        results = self.model(frame, conf=self.confidence_threshold)
        boxes, scores, num_people, density = self._postprocess_detections(
            results[0].boxes.xyxy, results[0].boxes.conf, frame.shape
        )
        stage = self._define_stage(density)
        fps = 1.0 / (time.time() - start_time)
        return DetectionResult(boxes, scores, num_people, density, stage, fps)

    def _postprocess_detections(self, boxes, scores, frame_shape):
        filtered_boxes = []
        filtered_scores = []
        for box, score in zip(boxes.tolist(), scores.tolist()):
            if score >= self.confidence_threshold:
                filtered_boxes.append(box)
                filtered_scores.append(score)
        num_people = len(filtered_boxes)
        frame_area = frame_shape[0] * frame_shape[1]
        density = num_people / frame_area if frame_area > 0 else 0
        return filtered_boxes, filtered_scores, num_people, density

    def _define_stage(self, density):
        if density < 0.00005:
            return "SMOOTH"
        elif density < 0.0001:
            return "CAREFUL"
        else:
            return "CROWDED"

def run_yolo_analysis():
    cap = cv2.VideoCapture("http://127.0.0.1:8000/live_feed/")
    detector = YOLOPeopleDetector("yolov8n.pt")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ 스트리밍 연결 실패")
            break

        result = detector.process_frame(frame)

        print(f"[YOLO] 인원: {result.num_people}, 밀집도: {result.density:.8f}, 단계: {result.stage}, FPS: {result.fps:.1f}")
