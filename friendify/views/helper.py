"""
Friendify helper functions.

URLs include:
/
"""
import flask, os, pprint
import friendify
import spotipy
import uuid


SCOPE = 'user-top-read'
pp = pprint.PrettyPrinter(indent=4)

def session_cache_path():
    return './.spotify_caches/' + flask.session['uuid']

def is_following(connection, username1, username2):
    cur = connection.execute(
        "SELECT COUNT(*) "
        "AS count FROM following WHERE username1=? "
        "AND username2=?;",
        (username1, username2,)
    )
    user = cur.fetchone()
    if user["count"] == 0:
        return False
    else:
        return True

def compare_score(connection, username1, username2):
    score  = 0
    total = 0

    cur = connection.execute(
        "SELECT COUNT(*) AS count "
        "FROM toptracks "
        "WHERE username=?;",
        (username1,)
    )

    count = cur.fetchone()
    total += count["count"]
    
    cur = connection.execute(
        "SELECT COUNT(*) AS count "
        "FROM topartists "
        "WHERE username=?;",
        (username1,)
    )

    count = cur.fetchone()
    total += count["count"]

    cur = connection.execute(
        "SELECT COUNT(*) as count "
        "FROM toptracks t1 INNER JOIN toptracks t2 ON t1.track=t2.track AND t1.username!=t2.username "
        "WHERE t1.username=? AND t2.username=?;",
        (username1, username2,)
    )
    count = cur.fetchone()
    score += count["count"]

    cur = connection.execute(
        "SELECT COUNT(*) as count "
        "FROM topartists a1 INNER JOIN topartists a2 ON a1.artist=a2.artist AND a1.username!=a2.username "
        "WHERE a1.username=? AND a2.username=?;",
        (username1, username2,)
    )
    count = cur.fetchone()
    score += count["count"]
    score = score / total * 100
    return score


def compare_artists(connection, username1, username2):
    cur = connection.execute(
        "SELECT a1.artist as name "
        "FROM topartists a1 INNER JOIN topartists a2 ON a1.artist=a2.artist AND a1.username!=a2.username "
        "WHERE a1.username=? AND a2.username=?;",
        (username1, username2,)
    )
    similar_artists = cur.fetchall()
    return similar_artists


def compare_tracks(connection, username1, username2):
    cur = connection.execute(
        "SELECT t1.track AS name, t1.artist AS artist "
        "FROM toptracks t1 INNER JOIN toptracks t2 ON t1.track=t2.track AND t1.username!=t2.username "
        "WHERE t1.username=? AND t2.username=?;",
        (username1, username2,)
    )
    similar_tracks = cur.fetchall()
    return similar_tracks


