"""
Friendify login view.

URLs include:
/
"""
import flask, os, uuid, pprint
import friendify
import spotipy
from friendify.views.helper import session_cache_path


@friendify.app.route('/', methods=['GET', 'POST'])
def show_index():
    pp = pprint.PrettyPrinter(indent=4)

    # Authenticate user
    if 'uuid' not in flask.session:
        print("uuid not in session, redirecting to login")
        return flask.redirect(flask.url_for('show_logout'))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_path=session_cache_path())
    if not auth_manager.get_cached_token():
        print("token not in cache, redirecting logging out")
        return flask.redirect(flask.url_for('show_logout'))

    # Connect to database
    connection = friendify.model.get_db()

    # Connect to Spotify API
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    username = spotify.me()["display_name"]
    tracks = spotify.current_user_top_tracks(20, 0, 'medium_term')['items']
    artists = spotify.current_user_top_artists(20, 0, 'medium_term')['items']

    # Load temporary data
    rank = 1
    for track in tracks:
        print(track["name"])
        track["image"] = track["album"]["images"][0]["url"]
        cur = connection.execute(
        "REPLACE INTO toptracks (username, track, rank)"
        " VALUES (?, ?, ?);",
        (username, track["name"], rank)
        )
        rank += 1
    rank = 1 
    for artist in artists:
        print(artist["name"])
        artist["image"] = artist["images"][0]["url"]
        cur = connection.execute(
        "REPLACE INTO topartists (username, artist, rank) "
        "VALUES (?, ?, ?);",
        (username, artist["name"], rank)
        )
        rank += 1

    # Handle add friend
    if flask.request.method == 'POST':
        if flask.request.form['username'] != "":
            print(username, flask.request.form['username'])
            cur = connection.execute(
                "INSERT INTO following "
                "VALUES (?, ?);",
                (username, flask.request.form['username'],)
            )
        return flask.redirect(flask.url_for('show_index'))

    # query all following of user_url_slug
    cur = connection.execute(
        "SELECT username2 as username "
        "FROM following "
        "WHERE username1=?;",
        (username,)
    )
    following_list = cur.fetchall()

    for following in following_list:
        # query if user is following back
        cur = connection.execute(
            "SELECT COUNT(username2) "
            "AS follow_back FROM following WHERE username1=?;",
            (following["username"],)
        )
        count_list = cur.fetchall()
        follow_back = 0
        for user in count_list:
            follow_back = user["follow_back"]
        if follow_back == 0:
            following["follow_back"] = 0
            continue
        else:
            following["follow_back"] = 1

    context = {}
    context["following_list"] = following_list
    context["username"] = username
    context["top_artists"] = artists
    context["top_tracks"] = tracks


    
    return flask.render_template("index.html", **context)

