#!/usr/bin/python3


import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class Development_Config(Config):
    DEBUG = True

config = {
    'development': Development_Config,
    'default': Development_Config
}
