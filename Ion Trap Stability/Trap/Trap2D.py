import numpy as _n
import copy
from Fields.Field2D import Field2D

class Trap2D(object):
    def __init__(self, trap_with_potential):
        self.trap = trap_with_potential
        self.steps_per_rf_period = 100
        self.sim_length_in_rf_period = 10000
        self.ion = None
        self.q_to_m = 0
        self.v = Field2D()
        self.p = Field2D()
        self.results = []

    def set_simulation_parameters(self, steps_per_rf_period, sim_length_in_rf_period):
        self.steps_per_rf_period = steps_per_rf_period
        self.sim_length_in_rf_period = sim_length_in_rf_period

    def set_ion(self, ion, p, v):
        self.ion = ion
        self.q_to_m = self.ion.charge / self.ion.mass
        self.p = p
        self.v = v

    def _get_acceleration(self, q, position):
        e_field = self.trap.get_e_field(q, position)
        e_field.mul_by(self.q_to_m)
        return e_field

    def start_simulation(self, is_quick = False):
        if self.ion == None:
            print("Ion not set!")
            return
        
        current_position = copy.copy(self.p)
        current_velocity = copy.copy(self.v)
        current_acceleration = Field2D()
        
        step_size = 1 / self.trap.f / self.steps_per_rf_period
        simulation_time = self.sim_length_in_rf_period / self.trap.f
        time_stamps_per_period = _n.arange(0, 1 / self.trap.f, step_size)
        q_per_period = [self.trap.get_q(t) for t in time_stamps_per_period]
        self.results = []

        current_time = 0
        current_index = 0

        self.results.append((current_time, current_position, current_velocity, current_acceleration))

        while current_time <= simulation_time:
            current_acceleration = self._get_acceleration(q_per_period[current_index % self.steps_per_rf_period], current_position)
            
            current_acceleration.mul_by(step_size)
            current_velocity.add_from(current_acceleration)
            current_acceleration.div_by(step_size)

            current_velocity.mul_by(step_size)
            current_position.add_from(current_velocity)
            current_velocity.div_by(step_size)
            
            current_time += step_size
            current_index += 1

            if not is_quick:
                self.results.append((current_time, copy.copy(current_position), copy.copy(current_velocity), copy.copy(current_acceleration)))

            if not current_position.in_bound(self.trap.trap_dim.r0, self.trap.trap_dim.side - self.trap.trap_dim.r0):
                return (current_time, False)

        return (current_time, True)