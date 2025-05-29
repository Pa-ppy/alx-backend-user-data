#!/usr/bin/env python3
""" Main Application Module """
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os
from api.v1.views import app_views
from models import storage
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth_type = os.getenv('AUTH_TYPE')

if auth_type == 'basic_auth':
    auth = BasicAuth()
elif auth_type == 'session_auth':
    auth = SessionAuth()
else:
    auth = Auth()


@app.before_request
def before_request():
    """Filter requests requiring authentication"""
    if auth is None:
        return
    excluded_paths = [
        "/api/v1/status/",
        "/api/v1/unauthorized/",
        "/api/v1/forbidden/",
        "/api/v1/auth_session/login/"
    ]
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
        abort(401)
    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close Storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 error"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 error"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 error"""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
