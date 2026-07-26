import os


class Config:
    SECRET_KEY = "AI_MEDICAL_SECRET_KEY"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    MODEL_FOLDER = os.path.join(BASE_DIR, "models")

    DATASET_FOLDER = os.path.join(BASE_DIR, "dataset")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS = {"csv"}
    
import os

class Config:
    SECRET_KEY = "medical-diagnosis-secret-key"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MODEL_FOLDER = os.path.join(BASE_DIR, "models")