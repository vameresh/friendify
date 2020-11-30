"""Interaction helper functions."""
import os
import flask
import friendify

def add_friend(connection, username):
    if flask.request.form['username'] != "" and flask.request.form['username'] != username:
        # add friend to db if doesn't already exist
        cur = connection.execute(
            "SELECT COUNT(*) as count FROM users "
            "WHERE username=?;",
            (flask.request.form['username'],)
        )

        count = cur.fetchone()
        if(count["count"] == 0):
            cur = connection.execute(
                "INSERT INTO users (username)"
                " VALUES (?);",
                (flask.request.form['username'],)
            )

        cur = connection.execute(
            "INSERT INTO following "
            "VALUES (?, ?);",
            (username, flask.request.form['username'],)
        )



def remove_friend(connection, username):
    if flask.request.form['username'] != "":
        cur = connection.execute(
            "DELETE FROM following "
            "WHERE username1=? AND username2=?;",
            (username, flask.request.form['username'],)
        )

