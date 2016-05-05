from types import FunctionType
from flask import request, jsonify, redirect, Blueprint

from .beam import analyse_beam
from .utilities import IFinder

beam_api = Blueprint('beam_api', __name__, template_folder='templates')


@beam_api.route('/calculate/beam', methods=['GET', 'POST'])
def calculate():
    if request.json:
        data = request.json['beam']
        beam_data = analyse_beam(data)
        return jsonify(beam_data)
    else:
        return redirect('/')


@beam_api.route('/calculate/second_area', methods=['GET', 'POST'])
def calculate_i():
    if request.json:
        data = request.json
        valid_shapes = [f for f in dir(IFinder) if isinstance(IFinder.__dict__.get(f), FunctionType)]
        if data['shape'] not in valid_shapes or 'shape' not in data:
            return jsonify({
                'error': 'Invalid shape'
            })
        ans = eval('IFinder.{fun}(*{args})'.format(fun=data['shape'], args=data['size']))
        return jsonify({
            'result': ans,
            'shape': data['shape'],
            'size': data['size']
        })
    else:
        return redirect('/')