from pydantic import BaseSettings


class Settings(BaseSettings):
    env: str = "dev"

    git_forge_url: str | None = None
    pm_tool_url: str | None = None
    matrix_homeserver: str | None = None

    llm_api_base: str | None = None
    llm_api_key: str | None = None

    class Config:
        env_prefix = "NUSY_"
        env_file = ".env"


settings = Settings()
