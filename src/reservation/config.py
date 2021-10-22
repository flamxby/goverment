import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    secret_key: str = os.environ.get("SECRET_KEY")
    algorithm: str = os.environ.get("ALGORITHM")
    access_token_expire_minutes: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    if 'postgres' in os.environ.get('DATABASE_URL'):
        database_url: str = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
    else:
        database_url: str = os.environ.get('DATABASE_URL')

settings = Settings()