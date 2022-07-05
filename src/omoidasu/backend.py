"""Backend for Omoidasu"""

import logging

import sqlalchemy
import appdirs

from omoidasu import config

logger = logging.getLogger(__name__)
logger.setLevel(config.logger_level)

user_state_dir = appdirs.user_state_dir(appname=config.APP_NAME,
                                        version=config.VERSION)
user_config_dir = appdirs.user_config_dir(appname=config.APP_NAME,
                                          version=config.VERSION)

# sqlalchemy.create_engine("sqlite:///db.sqlite")
