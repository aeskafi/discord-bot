import os
import logging
from threading import Thread

# Suppress verbose Flask request logs
logging.getLogger("werkzeug").setLevel(logging.ERROR)

def create_app():
    try:
        from flask import Flask, jsonify
        app = Flask(__name__)

        @app.route("/")
        def home():
            return jsonify({
                "status": "online",
                "service": "Discord Bot",
                "maintainer": "Arham Eskafi (arham.dev)"
            })

        return app
    except ImportError:
        return None

def run():
    app = create_app()
    if app:
        port = int(os.getenv("PORT", 8080))
        app.run(host="0.0.0.0", port=port)

def keep_alive():
    """Starts background health-check server if Flask is installed."""
    t = Thread(target=run, daemon=True)
    t.start()