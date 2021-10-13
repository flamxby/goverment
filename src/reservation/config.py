import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    secret_key: str = os.environ.get("SECRET_KEY")
    algorithm: str = os.environ.get("ALGORITHM")
    access_token_expire_minutes: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

settings = Settings()