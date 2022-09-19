#!/usr/bin/python3
"""Main enpoints"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Returs the status of the service"""
    return jsonify({"status": "OK"})
