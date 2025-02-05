import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

class TestConfig:
    TESTING = True
    DEBUG = True
