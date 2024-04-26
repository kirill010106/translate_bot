from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: str


@dataclass
class TranslateApi:
    token: str
    folder: str
    oauth: str


@dataclass
class Config:
    tg_bot: TgBot
    translate_api: TranslateApi


def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env("BOT_TOKEN"),
            admin_ids=env("admin_ids")
        ),
        translate_api=TranslateApi(
            token=env("IAM_TOKEN"),
            folder=env("folder_id"),
            oauth=env("OAUTH_TOKEN")
        )
    )
