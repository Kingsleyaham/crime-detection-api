import pathlib
from typing import Any

import cv2
import numpy as np
import torch
from huggingface_hub import hf_hub_download
from ultralytics import YOLO

from app.core.config import settings


class ViolenceDetectionService:
    def __init__(self,model_path: str = None, use_huggingface:bool = True):
        """
        Initialize teh violence detection service with the YOLO model.

        Args:
            model_path: Path to the YOLO model (optional).
        """
        if model_path is None:
            if use_huggingface:
                model_path = self._download_from_huggingface()
            else:
                base_path = pathlib.Path(__file__).parent.parent.parent.parent
                model_path =str(base_path / "data" / "best.pt")

        # Use GPU if available
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")
        # Use half precision for faster inference
        self.half = True if self.device == 'cuda' else False

        self.model = self._load_model(model_path)

        # YOLOv8 specific parameters
        self.input_size = (640, 640)
        self.confidence_threshold = 0.25

        # Move model to appropriate device
        if hasattr(self.model, 'to'):
            self.model = self.model.to(self.device)

    def _download_from_huggingface(self) -> str:
        """Download the model from HuggingFace repository"""
        try:
            print("Downloading model from HuggingFace...")
            model_path = hf_hub_download(repo_id=settings.HUGGING_REPO_ID, filename="best.pt", cache_dir="../models")

            print(f"Model downloaded to: {model_path}")
            return model_path
        except Exception as e:
            print(f"Error downloading from HuggingFace: {str(e)}")
            raise RuntimeError(f"Failed to download model from HuggingFace: {e}")

    def _load_model(self, model_path: str):
        """Load the YOLOv8 model."""
        try:
            print(f"Loading model from: {model_path}")
            model = YOLO(model_path)
            return model
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise RuntimeError(f"Failed to load model: {e}")

    def process_video(self, video_path: str) -> list[dict[Any, Any]]:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return [{"error": "Could not open video file."}]

        frames_results = []
        frame_count = 0
        batch_size = 4  # Process 4 frames at once
        batch_frames = []
        batch_indices = []

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Only process every Nth frame
            if frame_count % 10 == 0:
                processed_frame = self._preprocess_frame(frame)
                batch_frames.append(processed_frame)
                batch_indices.append(frame_count)

                # Process batch when it reaches the desired size
                if len(batch_frames) >= batch_size:
                    results = self.model(batch_frames, verbose=False)  # Add verbose=False to reduce logging

                    for i, result in enumerate(results):
                        frame_results = self._parse_result(result, batch_indices[i], batch_frames[i].shape)
                        frames_results.append(frame_results)

                    batch_frames = []
                    batch_indices = []

            frame_count += 1


        # Process any remaining frames in the last batch
        if batch_frames:
            results = self.model(batch_frames, verbose=False)
            for i, result in enumerate(results):
                frame_results = self._parse_result(result, batch_indices[i], batch_frames[i].shape)
                frames_results.append(frame_results)

        cap.release()
        return frames_results

    def _preprocess_frame(self, frame):
        """
             Preprocess a frame for the YOLOv8 model.
             For YOLOv8, we typically just need to ensure it's in the right format.
             """
        # YOLOv8 from Ultralytics can handle preprocessing internally
        # We just need to make sure the image is in BGR format (OpenCV default)
        resized_frame = cv2.resize(frame, (320, 320)) # Half the standard 640x640
        return resized_frame

    def _parse_result(self, results,  frame_number:int, original_shape: tuple)->dict[str, Any]:
        """Parse the model predictions into a standardized format"""
        violence_detected = False
        max_confidence = 0.0
        detections = []

        try:
            # Handle different possible formats of YOLOv8 results

            # If results is a list (common format for newer YOLOv8)
            if hasattr(results, 'boxes') and hasattr(results, 'names'):
                # Modern Ultralytics YOLO format
                boxes = results.boxes.cpu().numpy()
                for box in boxes:
                    # Extract data from the box
                    x1, y1, x2, y2 = box.xyxy[0]  # Box coordinates
                    confidence = box.conf[0]  # Confidence score
                    class_id = int(box.cls[0])  # Class ID
                    class_name = results.names[class_id]  # Class name

                    if confidence > self.confidence_threshold:
                        violence_detected = True
                        max_confidence = max(max_confidence, float(confidence))

                        detections.append({
                            "bbox": [float(x1), float(y1), float(x2), float(y2)],
                            "confidence": float(confidence),
                            "class_id": class_id,
                            "class_name": class_name
                        })

            # Alternative format for older YOLOv8 or pickle exports
            elif isinstance(results, np.ndarray) and results.ndim == 2:
                # Format: [x1, y1, x2, y2, confidence, class_id]
                for detection in results:
                    if len(detection) >= 6:  # Make sure we have all needed values
                        x1, y1, x2, y2, confidence, class_id = detection[:6]

                        if confidence > self.confidence_threshold:
                            violence_detected = True
                            max_confidence = max(max_confidence, float(confidence))

                            detections.append({
                                "bbox": [float(x1), float(y1), float(x2), float(y2)],
                                "confidence": float(confidence),
                                "class_id": int(class_id),
                                "class_name": f"class_{int(class_id)}"  # No class names available
                            })

            # Another possible format
            elif isinstance(results, list):
                for result in results:
                    if hasattr(result, 'boxes'):
                        # Process each result's boxes
                        for box in result.boxes.cpu().numpy():
                            # Similar processing as above
                            confidence = box.conf[0]
                            if confidence > self.confidence_threshold:
                                violence_detected = True
                                max_confidence = max(max_confidence, confidence)
                                # Add detection (similar to above)

            # Yet another possible format (plain dictionary)
            elif isinstance(results, dict) and 'predictions' in results:
                for pred in results['predictions']:
                    confidence = pred.get('confidence', 0)
                    if confidence > self.confidence_threshold:
                        violence_detected = True
                        max_confidence = max(max_confidence, confidence)
                        # Add detection with available data

        except Exception as e:
            return {
                "frame": frame_number,
                "error": f"Failed to parse predictions: {str(e)}"
            }

        return {
            "frame": frame_number,
            "violence_detected": violence_detected,
            "confidence": float(max_confidence),
            "detections": detections,
            "frame_size": {"height": original_shape[0], "width": original_shape[1]}
        }


    def detect_from_image(self, image_data):
        """Process a single image for violence/crime detection."""
        try:
            # Convert from bytes to OpenCV format if needed
            if isinstance(image_data, bytes):
                nparr = np.frombuffer(image_data, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            else:
                image = image_data

            # Get predictions
            results = self.model(image)

            # Resize image for faster processing
            image = cv2.resize(image, (320, 320))

            # Get predictions with optimized parameters
            results = self.model(image, half=self.half, verbose=False)

            # Parse results
            return self._parse_result(results, 0, image.shape)
        except Exception as e:
            return {"error": str(e)}
