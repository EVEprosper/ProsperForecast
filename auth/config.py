"""flask configuration tools"""
import os

import prosper.common.prosper_config as p_config

HERE = os.path.abspath(os.path.dirname(__file__))
LOCAL_CONFIG_PATH = os.path.join(HERE, 'config.j2')

class DefaultConfig(object):
    DEBUG = False
    SECRET_KEY = 'TODO'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/forecast.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_BLACKLIST_ENABLED = True
    JWT_BLAKCLIST_TOKEN_CHECKS = ['access', 'refresh']

    LOCAL_CONFIG = p_config.ProsperConfig(LOCAL_CONFIG_PATH)

class Cli(DefaultConfig):
    # LOCAL_CONFIG = p_config.render_secrets(
    #     LOCAL_CONFIG_PATH,
    #     os.environ.get('SECRET_CFG', ''),
    # )
    DEBUG = True
    JWT_LEEWAY = 3600

class Test(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True

class Production(DefaultConfig):
    try:
        LOCAL_CONFIG = p_config.render_secrets(
            LOCAL_CONFIG_PATH,
            os.environ.get('SECRET_CFG', ''),
        )
    except Exception as err:
        LOCAL_CONFIG = p_config.ProsperConfig(LOCAL_CONFIG_PATH)
