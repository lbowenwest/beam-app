valid_types = ['Simple', 'Roller', 'BuiltIn']


class Support(object):
    """
    docstring for base Support class
    """

    def __init__(self, _type='Simple', position=0):
        self._type = _type
        self._position = position

        self._vertical_reaction = 0
        self._horizontal_reaction = 0
        self._moment_reaction = 0

    def __str__(self):
        return '{type} Support:\n\tposition: {pos}\treactions: {reactions}\n'.format(
            type=self.type,
            pos=self.position,
            reactions=' '.join(['{} ({})'.format(r, self.reaction(r)) for r in self.reactions.keys() if self.reactions[r]])
        )

    def has_reaction(self, direction):
        """
        Check support has reaction to a direction
        :param direction: string representing direction
        :return: true is has reaction false if not
        """
        try:
            return self.reactions[direction]
        except KeyError as e:
            print(e)
            return False

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value if value in ['Simple', 'Roller', 'BuiltIn'] else self._type

    @property
    def reactions(self):
        if self.type == 'Simple':
            return {
                'horizontal': True,
                'vertical':     True,
                'moment':       False
            }
        elif self.type == 'Roller':
            return {
                'horizontal':   False,
                'vertical':     True,
                'moment':       False
            }
        elif self.type == 'BuiltIn':
            return {
                'horizontal':   True,
                'vertical':     True,
                'moment':       True
            }
        else:
            return {
                'horizontal': False,
                'vertical': False,
                'moment': False
            }

    def reaction(self, direction):
        if direction == 'vertical':
            return self.vertical_reaction
        elif direction == 'horizontal':
            return self.horizontal_reaction
        elif direction == 'moment':
            return self.moment_reaction
        else:
            return 0

    @property
    def num_reactions(self):
        return len([r for r in self.reactions.values() if r is True])

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value if value > 0 else self._position

    @property
    def vertical_reaction(self):
        return self._vertical_reaction if self.has_reaction('vertical') else 0

    @vertical_reaction.setter
    def vertical_reaction(self, value):
        self._vertical_reaction = value if self.has_reaction('vertical') else 0

    @property
    def horizontal_reaction(self):
        return self._horizontal_reaction if self.has_reaction('horizontal') else 0

    @horizontal_reaction.setter
    def horizontal_reaction(self, value):
        self._horizontal_reaction = value if self.has_reaction('horizontal') else 0

    @property
    def moment_reaction(self):
        return self._moment_reaction if self.has_reaction('moment') else 0

    @moment_reaction.setter
    def moment_reaction(self, value):
        self._moment_reaction = value if self.has_reaction('moment') else 0
