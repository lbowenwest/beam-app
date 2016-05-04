from types import FunctionType
from flask import render_template, request, jsonify, redirect

from . import beam_bp

from .beam import analyse_beam
from .utilities import IFinder


@beam_bp.route('/')
def index():
    return render_template('beam/index.html')


@beam_bp.route('/calculate/beam', methods=['GET', 'POST'])
def calculate():
    if request.json:
        data = request.json['beam']
        beam_data = analyse_beam(data)
        return jsonify(beam_data)
    else:
        return redirect('/')


@beam_bp.route('/calculate/second_area', methods=['GET', 'POST'])
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