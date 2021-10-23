import secrets

SECRET_KEY = secrets.token_urlsafe(32)
SERVER_HOST = "127.0.0.1"
PROJECT_NAME = "library_recommendation"
SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite3.db"
ALLOWED_HOSTS = ('localhost', '127.0.0.1', )
BACKEND_CORS_ORIGINS = False
