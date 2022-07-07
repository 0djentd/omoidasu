"""Authentication functions and utils."""


import appdirs

from .models import User


APP_NAME = "omoidasu"

DEFAULT_USER_STATE_DIR = appdirs.user_state_dir(appname=APP_NAME)
DEFAULT_USER_CONFIG_DIR = appdirs.user_config_dir(appname=APP_NAME)


def login(context, username: str, password: str) -> User | None:
    return get_user(context)


def logout(context) -> bool:
    return False


def get_user(context) -> User | None:
    return None
