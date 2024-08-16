from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # SettingsConfigDict: é um objeto do pydantic-settings
    # que carrega as variáveis em um arquivo de configuração.
    # Por exemplo, um .env.

    # O atributo extra='ignore' faz com que o Pydantic não pegue do .env
    # outras variáveis que não estão definidas nessa classe Settings
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
