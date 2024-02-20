#!/usr/bin/env python3
"""Basic flask app"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


AUTH = Auth()


app = Flask(__name__)


@app.route("/")
def home():
    """returns json"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """Register a user."""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "User created"})
    except ValueError:
        return jsonify({"message": "Email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """create a new session for the user,
    store it the session ID as a cookie"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session = AUTH.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie("session_id", session)
        return res
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Find the user with the requested session ID.
    If the user exists destroy the session and redirect
    the user to GET /"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        redirect(url_for('home'))
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
