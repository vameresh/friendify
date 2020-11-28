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

    # Connect to database
    connection = friendify.model.get_db()

    # Connect to Spotify API
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    username = spotify.me()["display_name"]

    # Delete the user top tracks
    cur = connection.execute(
        "DELETE FROM toptracks WHERE username=?;",
        (username,)
    )

    # Delete the user top artists
    cur = connection.execute(
        "DELETE FROM topartists WHERE username=?;",
        (username,)
    )

    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        flask.session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return flask.redirect(flask.url_for('show_login'))
