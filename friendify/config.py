"""
Friendify development configuration.
"""

import pathlib, os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

SECRET_KEY = os.urandom(64)
SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = './.flask_session/'

FRIENDIFY_ROOT = pathlib.Path(__file__).resolve().parent.parent


# Database file is var/insta485.sqlite3
DATABASE_FILENAME = FRIENDIFY_ROOT/'var'/'insta485.sqlite3'