"""
Friendify development configuration.
"""

import pathlib, os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

SECRET_KEY = b'\x9b\x18g\xb9A\xe6\xcfG\xae\x00d\xc9\xd8\x16U\x17w\xee\xac\x80\xa1\xb9\xf4\x1f'
SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = './.flask_session/'

FRIENDIFY_ROOT = pathlib.Path(__file__).resolve().parent.parent


# Database file is var/insta485.sqlite3
DATABASE_FILENAME = FRIENDIFY_ROOT/'var'/'friendify.sqlite3'