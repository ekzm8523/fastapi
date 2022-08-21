from pydantic import BaseSettings, Field
from pathlib import Path
import os


class DatabaseSettings(BaseSettings):
    host: str = Field(default="127.0.0.1", env="POSTGRES_HOST")
    port: int = Field(default=5432, env="POSTGRES_PORT")
    db: str = Field(default="mms", env="POSTGRES_DB")
    user: str = Field(default="mms_admin", env="POSTGRES_USER")
    password: str = Field(default="12345", env="POSTGRES_PASSWORD")

    def get_url(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class JWTSettings(BaseSettings):
    ...


class GithubOAuthSettings(BaseSettings):
    client_id: str = Field(env="GITHUB_OAUTH_CLIENT_ID")
    client_secret: str = Field(env="GITHUB_OAUTH_CLIENT_SECRET")

    class Config:
        env_file = os.path.join(os.path.dirname(Path(".").resolve()), '.env')


class GoogleOAuthSettings(BaseSettings):
    client_id: str = Field(env="GOOGLE_OAUTH_CLIENT_ID")
    client_secret: str = Field(env="GOOGLE_OAUTH_CLIENT_SECRET")

    class Config:
        env_file = os.path.join(os.path.dirname(Path(".").resolve()), '.env')


class ApplicationSettings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    stage: str = Field(default="local", env="STAGE")
    service_name: str = Field(default="/mms", env="SERVICE_NAME")
    jwt: JWTSettings = JWTSettings()
    github: GithubOAuthSettings = GithubOAuthSettings()
    google: GoogleOAuthSettings = GoogleOAuthSettings()

