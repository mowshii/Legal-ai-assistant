"""
app.py
--------
Application entrypoint. Intentionally thin — per the project spec, the
entire backend must NOT live inside this one file. It only creates the
Flask app, wires extensions, registers blueprints, and starts the server.

Run:
  python app.py
Or with the Flask CLI:
  flask --app app run --debug

Dependencies: Flask, Flask-CORS, Flask-JWT-Extended, SQLAlchemy (all in requirements.txt)
"""

import os
from flask import Flask, jsonify
from config import config
from extensions import db, jwt, cors

from routes.auth_routes import auth_bp
from routes.document_routes import document_bp
from routes.analysis_routes import analysis_bp
from routes.report_routes import report_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(config.REPORT_FOLDER, exist_ok=True)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS}})

    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(report_bp)

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    @app.errorhandler(413)
    def too_large(_err):
        return jsonify({"error": "Maximum file size is 10 MB."}), 413

    @app.errorhandler(404)
    def not_found(_err):
        return jsonify({"error": "Resource not found."}), 404

    @app.errorhandler(500)
    def server_error(_err):
        return jsonify({"error": "Internal server error."}), 500

    with app.app_context():
        db.create_all()  # For local dev. Use Alembic migrations in production.

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
