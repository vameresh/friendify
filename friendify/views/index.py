"""
Friendify login view.

URLs include:
/
"""
import flask, os, uuid, pprint
import friendify
import spotipy
from friendify.views.helper import session_cache_path, is_following
from friendify.views.helper import compare_score, compare_artists, compare_tracks
from friendify.views.interact import add_friend, remove_friend


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

    # assimilate user top data

    tracks = spotify.current_user_top_tracks(50, 0, 'medium_term')['items']
    artists = spotify.current_user_top_artists(50, 0, 'medium_term')['items']

    # Load temporary data
    rank = 1
    for track in tracks:
        # print(track["name"])
        track["image"] = track["album"]["images"][0]["url"]
        cur = connection.execute(
            "REPLACE INTO toptracks (username, track, artist, rank)"
            " VALUES (?, ?, ?, ?);",
            (username, track["name"], track["artists"][0]["name"], rank,)
        )
        rank += 1
        print(track["name"])
    rank = 1 
    for artist in artists:
        # print(artist["name"])
        artist["image"] = artist["images"][0]["url"]
        cur = connection.execute(
            "REPLACE INTO topartists (username, artist, rank) "
            "VALUES (?, ?, ?);",
            (username, artist["name"], rank,)
        )
        rank += 1

    # Handle add friend
    if flask.request.method == 'POST':
        if 'follow' in flask.request.form:
            add_friend(connection, username)
        if 'unfollow' in flask.request.form:
            remove_friend(connection, username)
        return flask.redirect(flask.url_for('show_index'))

    # query all following of user_url_slug
    cur = connection.execute(
        "SELECT following.username2 AS username, users.active AS active "
        "FROM following "
        "INNER JOIN users ON following.username2=users.username "
        "WHERE following.username1=? "
        "ORDER BY users.active DESC, users.username ASC",
        (username,)
    )
    following_list = cur.fetchall()

    pp.pprint(following_list)

    for following in following_list:
        # query if user is following back
        following["follows_back"] = is_following(connection, following["username"], username)
        if following["follows_back"] and following["active"]:
            following["score"] = compare_score(connection, following["username"], username)
            following["similar_artists"] = compare_artists(connection, following["username"], username)
            following["similar_tracks"] = compare_tracks(connection, following["username"], username)
            
    context = {}
    context["following_list"] = following_list
    context["username"] = username
    context["top_artists"] = artists[:20]
    context["top_tracks"] = tracks[:20]


    
    return flask.render_template("index.html", **context)

