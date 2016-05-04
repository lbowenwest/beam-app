from flask import Flask

app = Flask(__name__)


def register_blueprints(current_app):
    from .beam.routes import beam_bp

    current_app.register_blueprint(beam_bp)

register_blueprints(app)
