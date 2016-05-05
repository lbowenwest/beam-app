import os
from flask import Flask
from flask_webpack import Webpack


webpack = Webpack()

app = Flask(__name__)

params = {
    'WEBPACK_MANIFEST_PATH': os.path.join(os.getcwd(), 'build', 'manifest.json')
}

app.config.update(params)

webpack.init_app(app)


def register_blueprints(current_app):
    from .routes import routes
    from .beam.routes import beam_routes
    from .beam.api import beam_api

    current_app.register_blueprint(routes)
    current_app.register_blueprint(beam_routes, url_prefix='/beam')
    current_app.register_blueprint(beam_api, url_prefix='/api')

register_blueprints(app)
