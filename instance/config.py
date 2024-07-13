import os

FLASK_RUN_HOST = "0.0.0.0"
FLASK_RUN_PORT = 9000

class Config:
    DEBUG = False
    TESTING = False
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 86400

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
