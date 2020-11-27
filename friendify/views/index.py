"""
Friendify login view.

URLs include:
/
"""
import flask, os, uuid, pprint
import friendify
import spotipy
from friendify.views.helper import session_cache_path


@friendify.app.route('/')
def show_index():

    if 'uuid' not in flask.session:
        print("uuid not in session, redirecting to login")
        return flask.redirect(flask.url_for('show_login'))

    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_path=session_cache_path())

    if not auth_manager.get_cached_token():
        print("token not in cache, redirecting logging out")
        return flask.redirect(flask.url_for('show_logout'))


    spotify = spotipy.Spotify(auth_manager=auth_manager)

    tracks = spotify.current_user_top_tracks(20, 0, 'short_term')['items']
    artists = spotify.current_user_top_artists(20, 0, 'short_term')['items']
    pp = pprint.PrettyPrinter(indent=4)

    for track in tracks:
        track["image"] = track["album"]["images"][0]["url"]

    for artist in artists:
        artist["image"] = artist["images"][0]["url"]

    context = {}
    context["displayname"] = spotify.me()["display_name"]
    user_id = spotify.me()["id"]
    context["top_artists"] = artists
    context["top_tracks"] = tracks


    
    return flask.render_template("index.html", **context)

