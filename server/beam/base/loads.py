def return_load(**kwargs):
    if kwargs['_type'] == 'Point':
        load = PointLoad(**kwargs)
    elif kwargs['_type'] == 'Uniform':
        load = UniformLoad(**kwargs)
    else:
        print('Invalid type: returned default `PointLoad`')
        return PointLoad()
    return load


class PointLoad(object):
    """
    docstring for PointLoad class
    """
    def __init__(self, **kwargs):
        self._position = kwargs['position'] if 'position' in kwargs else 0
        self._force = kwargs['force'] if 'force' in kwargs else 0
        self._moment = kwargs['moment'] if 'moment' in kwargs else 0

    def __str__(self):
        return 'Point Load:\n\tposition: {pos}\tforce: {force}\tmoment: {moment}\n'.format(
            pos=self.position, force=self.force, moment=self.moment)

    @property
    def type(self):
        return 'Point'

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value if value >= 0 else self._position

    @property
    def force(self):
        return self._force

    @force.setter
    def force(self, value):
        self._force = value

    @property
    def moment(self):
        return self._moment

    @moment.setter
    def moment(self, value):
        self._moment = value


class UniformLoad(object):
    """
    docstring for UniformLoad
    """
    def __init__(self, **kwargs):
        """
        :param start: start position
        :param end: end position
        :param line: line pressure
        """
        self._start = kwargs['start'] if 'start' in kwargs else 0
        self._end = kwargs['end'] if 'end' in kwargs else 0
        self._line_pressure = kwargs['line_pressure'] if 'line_pressure' in kwargs else 0

    def __str__(self):
        return 'Uniform Load:\n\tstart: {start}\tend: {end}pressure: {line}\n'.format(
            start=self.start, end=self.end, line=self.line_pressure)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value if 0 < value < self._end else self._start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value if value > self._start else self._end

    @property
    def line_pressure(self):
        return self._line_pressure

    @line_pressure.setter
    def line_pressure(self, value):
        self._line_pressure = value

    @property
    def position(self):
        return (self.start + self.end) / 2

    @property
    def length(self):
        return self.end - self.start

    @property
    def force(self):
        return self.length * self.line_pressure

    @property
    def moment(self):
        return 0
