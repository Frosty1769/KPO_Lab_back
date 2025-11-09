from typing import ClassVar


class Settings():

    SECRET_KEY: str = "secret"
    CORS_ORIGINS: ClassVar[list[str]] = ["*"]
    CORS_ALLOW_HEADERS: ClassVar[list[str]] = ["Content-Type"]
    SESSION_TYPE: str = "filesystem"
    SESSION_COOKIE_SAMESITE: str = "Lax"
    # SESSION_COOKIE_SAMESITE: str = "None"
    # SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_SECURE: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SQLALCHEMY_DATABASE_URI="sqlite:///dnd-game.db"


settings = Settings()
