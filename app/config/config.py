from dotenv import load_dotenv
import os
load_dotenv()

class Config(object):
    """Config base class
    This is the default configuration class for your app. You should
    `probably` not use this directly, instead extend this class with
     your custom config for different environments
    """
    DEBUG = False
    TESTING = False
    ENV = 'development'


class DevelopmentConfig(Config):
    """Development Config
    This extends the `Config` base class to store variables
    for development environments
    """
    DEBUG = True
    FLASK_APP = 'APP-DEV'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_DEV')
    SECRET_KEY = os.getenv('SECRET_KEY')
    # uncomment to open the server to LAN!
    SERVER_NAME = '192.168.20.8:2000'
    PORT = os.getenv('PORT') or 2000

class TestingConfig(Config):
    """Testing Config
       This extends the `Config` base class to store variables
       for testing environments
       """
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_TESTING')


class StagingConfig(Config):
    """Staging Config
       This extends the `Config` base class to store variables
       for staging environments

       """
    pass


class ProductionConfig(Config):
    """Production Config
       This extends the `Config` base class to store variables
       for production environments

       """
    ENV = 'production'

