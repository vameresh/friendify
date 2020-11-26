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

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

@friendify.app.route('/accounts/login/')
def show_login():

    if 'uuid' not in flask.session:
        print("visitor is unknown")
        # Step 1. Visitor is unknown, give random ID
        flask.session['uuid'] = str(uuid.uuid4())

    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-top-read',
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

    print("logged in, redirecting to index page")
    return flask.redirect(flask.url_for('show_index'))
