from pydantic import Field
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# .envファイルを明示的に読み込む
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings
    """
    PROJECT_NAME: str = "FastAPI Application"
    PROJECT_DESCRIPTION: str = "A simple FastAPI application"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # OpenAI設定
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    OPENAI_MODEL_NAME: str = "gpt-4o"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
