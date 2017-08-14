import scipy.constants as _c
import numpy as _n

class TrapDimension(object):
    def __init__(self, r0, r_rods):
        self.r0 = float(r0)
        self.r_rods = float(r_rods)
        self.d_rods = 2 * self.r_rods
        self.diagonal = 2 * self.r0 + self.d_rods
        self.side = self.diagonal / _n.sqrt(2)
        self._calc_cap()

    def _calc_cap(self):
        self.c_next_value = _n.pi * _c.epsilon_0 / _n.log(self.side / self.d_rods + _n.sqrt(_n.power(self.side / self.d_rods, 2) - 1))
        self.c_diag_value = _n.pi * _c.epsilon_0 / _n.log(self.diagonal / self.d_rods + _n.sqrt(_n.power(self.diagonal / self.d_rods, 2) - 1))

    @property
    def c_next(self):
        return self.c_next_value

    @property
    def c_diag(self):
        return self.c_diag_value