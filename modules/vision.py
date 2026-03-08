import pytesseract
from PIL import Image
import os
from modules.utils import get_logger

logger = get_logger("Vision")

class VisionEngine:
    def __init__(self, config):
        self.config = config
        # Placeholder for TFLite model
        self.tflite_model_path = "models/yolo.tflite"

    def perform_ocr(self, image_path):
        if not os.path.exists(image_path):
            logger.error(f"Image not found: {image_path}")
            return ""

        logger.info(f"Performing OCR on {image_path}...")
        try:
            text = pytesseract.image_to_string(Image.open(image_path))
            return text.strip()
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return ""

    def detect_objects(self, image_path):
        # Placeholder for TFLite Object Detection
        logger.info(f"Detecting objects in {image_path}...")
        # Mock result
        return [{"label": "stove", "confidence": 0.85, "bbox": [10, 20, 100, 200]}]

    def understand_scene(self, image_path):
        ocr_text = self.perform_ocr(image_path)
        objects = self.detect_objects(image_path)

        summary = f"Scene contains: {', '.join([o['label'] for o in objects])}. "
        if ocr_text:
            summary += f"Detected text: {ocr_text[:50]}..."

        return summary
