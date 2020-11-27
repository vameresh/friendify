"""
Friendify login view.

URLs include:
/
"""
import flask, os
import friendify
import spotipy
import uuid
from friendify.views.helper import session_cache_path


@friendify.app.route('/accounts/logout/')
def show_logout():

    if 'uuid' not in flask.session:
        print("uuid not in session, redirecting to login")
        return flask.redirect(flask.url_for('show_login'))

    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_path=session_cache_path())

    if not auth_manager.get_cached_token():
        print("token not in cache, redirecting to login")
        return flask.redirect(flask.url_for('show_login'))

    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        flask.session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return flask.redirect(flask.url_for('show_login'))
