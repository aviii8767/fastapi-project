from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #List of Env Variables, pydantic class
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        #env_file = Path(__file__).parent / ".env"  # Always resolves to app/.env


settings = Settings()
# print("Loaded settings:", settings.dict())
