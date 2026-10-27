"""Estimate traffic queues with object detection on sampled video frames."""
from functools import lru_cache
from threading import Lock

import cv2
import numpy as np
from ultralytics import YOLO

from config import DETECTION_CONFIDENCE, DETECTION_SAMPLE_INTERVAL_SECONDS, ROI, VEHICLE_CLASSES

_inference_lock = Lock()


@lru_cache(maxsize=1)
def _vehicle_detector():
    return YOLO("yolo11n.pt")


def count_vehicles(video_path):
    """Return the 75th-percentile vehicle count from sampled frames."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    try:
        fps = cap.get(cv2.CAP_PROP_FPS)
        sample_every = max(round(fps * DETECTION_SAMPLE_INTERVAL_SECONDS), 1)
        detector = _vehicle_detector()
        counts = []
        frame_index = 0

        while True:
            ok, frame = cap.read()
            if not ok:
                break

            if frame_index % sample_every == 0:
                height, width = frame.shape[:2]
                x1, y1 = int(ROI[0] * width), int(ROI[1] * height)
                x2, y2 = int(ROI[2] * width), int(ROI[3] * height)
                image = frame[y1:y2, x1:x2]
                if image.size == 0:
                    raise ValueError("Configured traffic region is empty for this video.")

                with _inference_lock:
                    result = detector.predict(
                        image,
                        classes=VEHICLE_CLASSES,
                        conf=DETECTION_CONFIDENCE,
                        imgsz=640,
                        verbose=False,
                    )[0]
                counts.append(len(result.boxes))

            frame_index += 1

        if not counts:
            raise ValueError(f"No frames could be read from video: {video_path}")
        return float(np.percentile(counts, 75))
    finally:
        cap.release()
