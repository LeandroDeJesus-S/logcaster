from pydantic_settings import BaseSettings, SettingsConfigDict


class DiscordEnvironmentVars(BaseSettings):
    api_token: str
    app_id: int
    client_secret: str
    public_key: str
    webhook_url: str


class Environment(BaseSettings):
    discord: DiscordEnvironmentVars

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        env_nested_delimiter='__'
    )
