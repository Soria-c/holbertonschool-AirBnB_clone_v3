#!/usr/bin/python3
"""Main"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def close():
    "Closes the db connection"
    storage.close()

@app_views.route('/status')
def status():
    """Returs the status of the service"""
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    ip = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    app.run(host=ip or '0.0.0.0' , port=port or 5000, threaded=True)
