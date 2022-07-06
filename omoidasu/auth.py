import appdirs


APP_NAME = "omoidasu"

DEFAULT_USER_STATE_DIR = appdirs.user_state_dir(appname=APP_NAME)
DEFAULT_USER_CONFIG_DIR = appdirs.user_config_dir(appname=APP_NAME)
