from numpy import array as a
import numpy as np
import sympy as sp


class Section(object):
    def __init__(self, start, end):
        self._start = start
        self._end = end

    def __str__(self):
        return "Start: {} End: {}".format(self.start, self.end)

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def contains(self, x):
        return self.start < x < self.end


class Beam(object):
    """
    docstring for Beam class
    """

    def __init__(self, length=1):
        self._length = length
        self._points = []

        self.loads = []
        self.supports = []

        self._sf_eqs = []
        self._sf_eval = []
        self._bm_eqs = []
        self._bm_eval = []

        self._update_points()

    def _load_moments(self, point=0):
        return np.sum(a([[l.force * (l.position - point)] for l in self.loads]))

    def _update_points(self):
        positions = []
        for load in self.loads:
            if load.type is 'Point':
                positions.append(load.position)
            elif load.type is 'Uniform':
                positions.extend([load.start_pos, load.end])
        for support in self.supports:
            positions.append(support.position)
        positions.sort()
        self._points = list(set(positions))

    def add_supports(self, *supports):
        """
        Appends supports to class supports list, then updates points
        :param supports: supports to add
        :return: updated support list
        """
        self.supports += supports
        self._update_points()
        return self.supports

    def remove_supports(self, *supports):
        """
        Checks each support in supports list, then removes and updates points
        :param supports: supports to remove
        :return:
        """
        for support in supports:
            if support in self.supports:
                self.supports.remove(support)
        self._update_points()

    def add_loads(self, *loads):
        """
        Appends loads to class loads list, then updates points
        :param loads: loads to add
        :return: updated load list
        """
        self.loads += loads
        self._update_points()
        return self.loads

    def remove_loads(self, *loads):
        """
        Checks if each load in class list, then removes and updates points
        :param loads:
        :return:
        """
        for load in loads:
            if load in self.loads:
                self.loads.remove(load)
        self._update_points()

    @property
    def points(self):
        self._points.sort()
        return self._points

    @property
    def sections(self):
        return [Section(self.points[idx], self.points[idx + 1]) for idx, val in enumerate(self.points[:-1])]

    @property
    def num_sections(self):
        return len(self.sections)

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value if value > 0 else self._length

    @property
    def num_supports(self):
        return len(self.supports)

    @property
    def num_reactions(self):
        return sum([s.numReactions for s in self.supports])

    @property
    def reactions(self):
        self._resolve()
        return a([s.vertical_reaction for s in self.supports])

    @property
    def num_loads(self):
        return len(self.loads)

    @property
    def vertical_loads(self):
        return a([l.force for l in self.loads])

    def _resolve(self):
        # TODO: Add horizontal and moment reaction support
        # TODO: Fix sign convention
        """
        There must be a better way!!!
        Currently only supports vertical resolving
        """
        eqs = []
        support_syms = sp.symbols('s0:{}'.format(self.num_supports))
        eq = -np.sum(self.vertical_loads)
        for s in support_syms:
            eq += s
        eqs.append(eq)

        for idx, sup in enumerate(self.supports):
            eq = self._load_moments(sup.position)
            for i, s in enumerate(support_syms):
                if i is idx:
                    continue
                eq -= s * (self.supports[i].position - sup.position)
            eqs.append(eq)
        solution = sp.linsolve(eqs, support_syms)

        for idx, val in enumerate(list(solution)[0]):
            self.supports[idx].vertical_reaction = val

    def calculate_shear_force(self):
        # TODO: Fix sign convention
        """
        Calculates shear force equations for each section of beam
        :return: list of `sympy` equations
        """
        self._resolve()
        eqs = []
        x = sp.Symbol('x')
        for section in self.sections:
            force = 0
            for load in self.loads:
                if load.type == 'Point' and load.position < section.end:
                    force -= load.force
                elif load.type == 'Uniform' and load.start > section.start:
                    force -= load.line_pressure * (x - section.start)
                    if load.end < section.end:
                        force += load.line_pressure * (x - section.end)
            for support in self.supports:
                if support.position < section.end:
                    force += support.vertical_reaction

            eqs.append(force)
        self._sf_eqs = eqs
        self._sf_eval = [sp.lambdify(x, eq, "numpy") for eq in eqs]
        return eqs

    @property
    def shear_force_eqs(self):
        return [sp.latex(eq) for eq in self._sf_eqs]

    @property
    def shear_force_values(self):
        return np.array([self._sf_eval[i](np.linspace(s.start, s.end)) for i, s in enumerate(self.sections)])

    def calculate_bending_moment(self):
        # TODO: Fix sign convention
        """
        Calculates bending moment equations for each section of beam
        :return: list of `sympy` equations
        """
        self._resolve()
        eqs = []
        x = sp.Symbol('x')
        for section in self.sections:
            moment = 0
            for load in self.loads:
                moment += load.moment
                if load.type is 'Point' and load.position < section.end:
                    moment += load.force * (x - load.position)
                if load.type is 'Uniform' and load.start > section.start:
                    moment += load.line_pressure * (x - load.start) ** 2 / 2
                    if load.end < section.end:
                        moment -= load.line_pressure * (x - load.end) ** 2 / 2

            for support in self.supports:
                if support.position < section.end:
                    moment -= support.vertical_reaction * (x - support.position)

            eqs.append(moment)
        self._bm_eqs = eqs
        self._bm_eval = [sp.lambdify(x, eq, "numpy") for eq in eqs]
        return eqs

    @property
    def bending_moment_eqs(self):
        return [sp.latex(eq) for eq in self._bm_eqs]

    @property
    def bending_moment_values(self):
        return np.array([self._bm_eval[i](np.linspace(s.start, s.end)) for i, s in enumerate(self.sections)])

    def calculations(self):
        self.calculate_shear_force()
        self.calculate_bending_moment()


def generate_beam_from_json(data):
    from .base import supports, loads

    length = data['length'] if 'length' in data else 1
    temp_supports = [supports.Support(**s) for s in data['supports']] if 'supports' in data else []
    temp_loads = [loads.return_load(**l) for l in data['loads']] if 'loads' in data else []

    beam = Beam(length)
    beam.add_supports(*temp_supports)
    beam.add_loads(*temp_loads)

    return beam


def analyse_beam(data):
    beam = generate_beam_from_json(data)

    beam.calculations()

    sections = [(section.start, section.end) for section in beam.sections]
    distance = a([np.linspace(section.start, section.end) for section in beam.sections])

    return {
        'sections': sections,
        'distance': [distance[i].tolist() for i in range(beam.num_sections)],
        'shear_force': {
            'equations': beam.shear_force_eqs,
            'values': [beam.shear_force_values[i].tolist() for i in range(beam.shear_force_values.shape[0])],
            'plot': {
                'x': distance.reshape(-1).tolist(),
                'y': beam.shear_force_values.reshape(-1).tolist(),
                'backup': {
                    'x': a([np.linspace(s.start, s.end) for s in beam.sections]).reshape(-1).tolist(),
                    'y': a([np.linspace(beam.shear_force_values[i], beam.shear_force_values[i]) for i in
                            range(beam.num_sections)]).reshape(-1).tolist()
                }
            }
        },
        'bending_moment': {
            'equations': beam.bending_moment_eqs,
            'values': [beam.bending_moment_values[i].tolist() for i in range(beam.bending_moment_values.shape[0])],
            'plot': {
                'x': distance.reshape(-1).tolist(),
                'y': beam.bending_moment_values.reshape(-1).tolist()
            }
        }
    }
