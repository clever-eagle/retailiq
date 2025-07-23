import os
from datetime import timedelta


class Config:
    """
    Application configuration
    """

    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key-here"
    DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

    # CORS settings
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = {"csv", "xlsx", "json"}

    # Model settings
    DEFAULT_MIN_SUPPORT = 0.01
    DEFAULT_MIN_CONFIDENCE = 0.2
    DEFAULT_MIN_LIFT = 1.0
    DEFAULT_FORECAST_DAYS = 30

    # Cache settings
    CACHE_TIMEOUT = timedelta(hours=1)

    # API rate limiting
    RATELIMIT_STORAGE_URL = "memory://"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
