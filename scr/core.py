from typing import ClassVar


class Settings():

    SECRET_KEY: str = "cashier_secret_key_2025"
    CORS_ORIGINS: ClassVar[list[str]] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    CORS_ALLOW_HEADERS: ClassVar[list[str]] = ["Content-Type"]
    SESSION_TYPE: str = "filesystem"
    SESSION_COOKIE_SAMESITE: str = "Lax"
    SESSION_COOKIE_HTTPONLY: bool = False
    SESSION_COOKIE_NAME: str = "cashier_session"
    PERMANENT_SESSION_LIFETIME: int = 3600  # 1 час
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SQLALCHEMY_DATABASE_URI = "sqlite:///cashier.db"


settings = Settings()
