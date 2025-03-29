import os
import tempfile
from typing import Any

import cv2
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException

from app.api.services.violence_detection_service import ViolenceDetectionService

router = APIRouter()


def get_service():
    """Dependency to get the YOLOv8 detection service."""
    return ViolenceDetectionService()


@router.post("/video", response_model=dict[str, list[dict[str, Any]]])
async def detect_violence_from_video(file: UploadFile = File(...), confidence: float | None = Form(0.25),
                                     service: ViolenceDetectionService = Depends(get_service)):
    """
       Detect violence/crime in a video file.

       - **file**: The video file to analyze
       - **confidence**: Optional confidence threshold (default: 0.25)

       Returns a list of results for processed frames.
    """
    # Validate file type
    if not file.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="File must be a video")

    # Update confidence threshold if provided
    service.confidence_threshold = confidence

    # Save the uploaded file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        contents = await file.read()
        with open(temp_file.name, 'wb') as f:
            f.write(contents)

        # Get video info
        cap = cv2.VideoCapture(temp_file.name)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        # Process the video
        results = service.process_video(temp_file.name)

        print('results', results)
        return {"results": results, "metadata": {
            "total_frames": total_frames,
            "processed_frames": len(results),
            "file_size_mb": round(os.path.getsize(temp_file.name) / (1024 * 1024), 2)
        }}
    finally:
        # Clean up the temp file
        temp_file.close()
        os.unlink(temp_file.name)


@router.post("/image", response_model=dict[str, Any])
async def detect_from_image(
        file: UploadFile = File(...),
        confidence: float | None = Form(0.25),
        service: ViolenceDetectionService = Depends(get_service)
):
    """
    Detect violence/crime in an image.

    - **file**: The image file to analyze
    - **confidence**: Optional confidence threshold (default: 0.25)

    Returns detection results for the image.
    """
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Update confidence threshold if provided
    service.confidence_threshold = confidence

    # Read the image file
    contents = await file.read()
    result = service.detect_from_image(contents)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result
