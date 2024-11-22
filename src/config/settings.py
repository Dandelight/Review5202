from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Keys
    ANTHROPIC_API_KEY: str

    # Directories
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    PAPERS_DIR: Path = DATA_DIR / "papers"
    MARKDOWN_DIR: Path = DATA_DIR / "markdown"
    SUMMARIES_DIR: Path = DATA_DIR / "summaries"
    PROMPT_PATH: Path = BASE_DIR / "Thinking-Claude/model_instructions/v4-20241118.md"

    # LLM Settings
    MODEL_NAME: str = "claude-3-sonnet-20240229"
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.3

    class Config:
        env_file = ".env"


settings = Settings()
