"""
Friendify login view.

URLs include:
/
"""
import flask, os, json, uuid
import friendify
import spotipy
from friendify.views.helper import session_cache_path, SCOPE

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

@friendify.app.route('/accounts/login/')
def show_login():

    if 'uuid' not in flask.session:
        print("visitor is unknown")
        # Step 1. Visitor is unknown, give random ID
        flask.session['uuid'] = str(uuid.uuid4())

    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=SCOPE,
                                                cache_path=session_cache_path(), 
                                                show_dialog=True)
    print("created auth manager")
    if flask.request.args.get("code"):
        auth_manager.get_access_token(flask.request.args.get("code"))
        print("redirected from spotify auth page")
        return flask.redirect(flask.url_for('show_login'))

    if not auth_manager.get_cached_token():
        print("no cached token yet, serving login")
        auth_url = auth_manager.get_authorize_url()
        context = {}
        context["auth_url"] = auth_url
        return flask.render_template("/accounts/login.html", **context)

    
    # Connect to database
    connection = friendify.model.get_db()

    # Connect to Spotify API
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    username = spotify.me()["display_name"]

    # Check if user exists
    cur = connection.execute(
        "SELECT COUNT(*) AS count FROM users WHERE username=?",
        (username,)
    )

    count = cur.fetchone()
    if(count["count"] == 0):
        # new user
        cur = connection.execute(
            "INSERT INTO users (username, active) VALUES(?,?)",
            (username, True,)
        )
    else:
        # update user
        cur = connection.execute(
            "UPDATE users SET active=? WHERE username=?;",
            (True, username,)
        )

    # Log in
    print("logged in, redirecting to index page")
    return flask.redirect(flask.url_for('show_index'))
