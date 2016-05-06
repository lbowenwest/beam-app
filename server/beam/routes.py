from flask import render_template, Blueprint

beam_routes = Blueprint('beam_routes', __name__ + '_routes', template_folder='templates')


@beam_routes.route('/', defaults={'path': ''})
@beam_routes.route('/<path:path>')
def index(path):
    return render_template('main/index.html')
