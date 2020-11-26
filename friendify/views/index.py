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


@friendify.app.route('/')
def show_index():

    if 'uuid' not in flask.session:
        print("uuid not in session, redirecting to login")
        return flask.redirect(flask.url_for('show_login'))

    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_path=session_cache_path())

    if not auth_manager.get_cached_token():
        print("token not in cache, redirecting to login")
        return flask.redirect(flask.url_for('show_login'))

    print("visitor has signed in already, serving index")
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    context = {}
    context["top_artists"] = spotify.current_user_top_artists()['items']
    context["top_tracks"] = spotify.current_user_top_tracks()['items']
    context["username"] = spotify.me()["display_name"]

    print(context["top_artists"])
    
    return flask.render_template("index.html", **context)

