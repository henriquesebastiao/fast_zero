from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # SettingsConfigDict: é um objeto do pydantic-settings
    # que carrega as variáveis em um arquivo de configuração.
    # Por exemplo, um .env.
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str
