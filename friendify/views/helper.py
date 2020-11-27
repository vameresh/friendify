"""
Friendify helper functions.

URLs include:
/
"""
import flask, os
import friendify
import spotipy
import uuid


SCOPE = 'user-top-read'

def session_cache_path():
    return './.spotify_caches/' + flask.session['uuid']