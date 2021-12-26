from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    host: str = Field(default="127.0.0.1", env="POSTGRES_HOST")
    port: int = Field(default=5432, env="POSTGRES_PORT")
    db: str = Field(default="harmony_product", env="POSTGRES_DB")
    user: str = Field(default="mms_admin", env="POSTGRES_USER")
    password: str = Field(default="12345", env="POSTGRES_PASSWORD")

    def get_url(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
