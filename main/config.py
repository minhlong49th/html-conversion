"""
Configuration settings for the Flask application.
"""

# # Flask configuration
# FLASK_APP = 'app.py'
# FLASK_ENV = 'development'

# # Database configuration
# # SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
# # SQLALCHEMY_TRACK_MODIFICATIONS = False

# # Secret key for session management
# SECRET_KEY = 'U9pHQIWMaDQMU9HiJnDkITlDoCGmXOzj'

# # Debug mode configuration
# DEBUG = True

# # Logging configuration
# LOG_LEVEL = 'DEBUG'

# # Flask-Run configuration
# FLASK_RUN_PORT = 8000

# # Other configuration settings
# MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Maximum file upload size (16MB)
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'U9pHQIWMaDQMU9HiJnDkITlDoCGmXOzj')
    DEBUG = False

class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Logging configuration
    LOG_LEVEL = 'DEBUG'
    # Flask-Run configuration
    FLASK_RUN_PORT = 8000
    SERVER_NAME = 'localhost:8000' or '127.0.0.1:8000'

class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY