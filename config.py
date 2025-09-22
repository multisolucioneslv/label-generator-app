import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Google Maps API Configuration
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    GOOGLE_API_ENABLED = os.getenv('GOOGLE_API_ENABLED', 'false').lower() == 'true'

    # MySQL Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'label_generator_db')
    DB_PORT = int(os.getenv('DB_PORT', 3306))

    # Application Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # Database URL for SQLAlchemy
    @property
    def DATABASE_URL(self):
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Application Settings
    MAX_LABELS_PER_DAY = int(os.getenv('MAX_LABELS_PER_DAY', 100))
    AUTO_APPROVE_USERS = os.getenv('AUTO_APPROVE_USERS', 'false').lower() == 'true'
    REQUIRE_TRACKING = os.getenv('REQUIRE_TRACKING', 'false').lower() == 'true'

# Global config instance
config = Config()