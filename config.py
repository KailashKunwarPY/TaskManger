# In config.py, ensure this:
import os
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).parent.parent
    INSTANCE_PATH = BASE_DIR / 'instance'
    INSTANCE_PATH.mkdir(exist_ok=True)
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{INSTANCE_PATH}/taskmanager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False