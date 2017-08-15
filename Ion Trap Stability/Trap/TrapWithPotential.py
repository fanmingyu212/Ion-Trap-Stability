from Trap.TrapDimension import TrapDimension
from Fields.Field2D import Field2D
import numpy as _n
import scipy.constants as _c

class TrapWithPotential(object):
    def __init__(self, trap_dim):
        self.trap_dim = trap_dim
        self.v_rf = 0
        self.f = 0
        self.omega = 0
        self.phase = 0
        self.v_biases = [0, 0, 0, 0]

    def set_rf(self, v_rf, f, phase=0):
        self.v_rf = v_rf
        self.f = f
        self.omega = self.f * 2 * _n.pi
        self.phase = phase / 360.0 * 2 * _n.pi

    def set_bias(self, v_biases):
        if len(v_biases) == 4:
            self.v_biases = v_biases

    def _get_v_rf(self, t):
        return self.v_rf * _n.cos(self.omega * t + self.phase)

    def _get_v_diffs(self, t):
        v_rf_now = self._get_v_rf(t)
        v1 = self.v_biases[1] - (v_rf_now + self.v_biases[0])
        v2 = (self.v_biases[2] + v_rf_now) - self.v_biases[1]
        v3 = self.v_biases[3] - (v_rf_now + self.v_biases[2])
        return [v1, v2, v3]

    def get_q(self, t):
        v_diffs = self._get_v_diffs(t)
        v1 = v_diffs[0]
        v2 = v_diffs[1]
        v3 = v_diffs[2]

        c_next = self.trap_dim.c_next
        c_diag = self.trap_dim.c_diag

        q1 = c_next * v1 + c_diag * (v1 + v2) + c_next * (v1 + v2 + v3)
        q2 = c_next * v2 + c_diag * (v2 + v3) - c_next * v1
        q3 = c_next * v3 - c_diag * (v1 + v2) - c_next * v2
        q4 = -c_next * (v1 + v2 + v3) - c_diag * (v2 + v3) - c_next * v1

        return [q1, q2, q3, q4]

    def get_e_field(self, q, position):
        q1 = q[0]
        q2 = q[1]
        q3 = q[2]
        q4 = q[3]

        x = position.x
        y = position.y
        side = self.trap_dim.side

        x_sq = _n.power(x, 2)
        y_sq = _n.power(y, 2)
        x_inv_sq = _n.power((side - x), 2)
        y_inv_sq = _n.power((side - y), 2)

        e_field = Field2D()
        e_field.x = q1 / (x_sq + y_sq) * y \
                    + q2 / (x_inv_sq + y_sq) * y \
                    + q3 / (x_inv_sq + y_inv_sq) * (y - side) \
                    + q4 / (x_sq + y_inv_sq) * (y - side)
        e_field.y = q1 / (x_sq + y_sq) * (-x) \
                    + q2 / (x_inv_sq + y_sq) * (side - x) \
                    + q3 / (x_inv_sq + y_inv_sq) * (side - x) \
                    + q4 / (x_sq + y_inv_sq) * (-x)
        e_field.div_by(_c.epsilon_0 * 2 * _n.pi)

        return e_field