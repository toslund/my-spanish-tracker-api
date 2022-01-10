import secrets, os, configparser
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    # For using a .ini file
    # config = configparser.ConfigParser()
    # config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    # config.read(config_path)

    #
    ## GENERAL
    #
    PROJECT_NAME: str = "TrackMySpanish"
    API_V1_STR: str = "/api/v1"
    USERS_OPEN_REGISTRATION: bool = os.getenv('USERS_OPEN_REGISTRATION', False) == 'true'
    DECKS_OPEN_POST: bool = os.getenv('DECKS_OPEN_POST', False) == 'true'
    OPEN_POST_KEY = os.getenv('OPEN_POST_KEY', secrets.token_urlsafe(32))

    #
    ## DROPBOX
    #
    dropbox_token = os.getenv('DBX_TOKEN')

    #
    ## SECURITY
    #
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    POST_QUESTION_TOKEN_EXPIRES_SECONDS: int = 60 * 60
    POST_QUESTION_TOKEN_NBF_SECONDS: int = os.getenv('NBF_SECONDS')

    #
    ## SERVER
    #
    # SERVER_NAME: str = www.example.com
    SERVER_HOST: str = os.getenv('SERVER_HOST')
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost", "http://localhost:8080", "https://trackmyspanish.com", "https://www.trackmyspanish.com", "https://unruffled-pasteur-6120ac.netlify.app"]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    #
    ## DATABASE
    #
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') if not os.getenv('DEV_MODE', 'false').lower() == 'true' else os.getenv('DATABASE_URL')
    # Hack to fix url supplied by heroku
    DEV_MODE = os.getenv('DEV_MODE', 'false').lower() == 'true'
    PRODUCTION_MODE = not DEV_MODE
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace("postgres://", "postgresql://", 1) if PRODUCTION_MODE else os.getenv('DATABASE_URL')
    #For manual setup
    # POSTGRES_SERVER: Optional[str] = None
    # POSTGRES_USER: Optional[str] = None
    # POSTGRES_PASSWORD: Optional[str] = None
    # POSTGRES_DB: Optional[str] = None

    #TODO delete following method for getting dev db
    # dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    # default_test_db = os.path.join(dir_path, 'dev.db')
    # SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.abspath(default_test_db)}'

    # @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgresql",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER"),
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )

    #
    ## EMAIL
    #

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_VERIFY_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "./app/templates"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

        

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore

    #
    ## FIRST USER
    #

    FIRST_SUPERUSER: EmailStr = os.getenv('SUPERUSER_EMAIL')
    FIRST_SUPERUSER_PASSWORD: str = os.getenv('SUPERUSER_PASSWORD')

    class Config:
        case_sensitive = True


settings = Settings()
