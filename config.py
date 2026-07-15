import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Basic configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'profile_photos')

    # Database configuration
    # 1. Fetch the URL from Render's environment variable
    db_url = os.environ.get('DATABASE_URL')

    # 2. Adjust for SQLAlchemy's requirement of 'postgresql://' instead of 'postgres://'
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    # 3. Set the URI: Use Render's URL if available, otherwise use your local MySQL
    SQLALCHEMY_DATABASE_URI = db_url or 'mysql+pymysql://root:151042@localhost:3306/skillswap'