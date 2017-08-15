import matplotlib.pyplot as plt
from multiprocessing import Pool
import copy

from Trap.TrapDimension import TrapDimension
from Trap.TrapWithPotential import TrapWithPotential
from Trap.Trap2D import Trap2D
from Ions.Sr88Ion import Sr88Ion
from Fields.Field2D import Field2D

def run_simulation(trap):
    return trap.start_simulation(True)

if __name__ == "__main__":
    pool = Pool(16) 

    r0 = 3e-3
    r_rod = 2.5e-3
    dim = TrapDimension(r0, r_rod)
    side = dim.side

    run_parallel = False

    if run_parallel:
        trap_pool = []
        for i in range(100):
            trap_with_pot_temp = TrapWithPotential(dim)
            v_rf_temp = 10 + i
            offset = -0.2
            trap_with_pot_temp.set_rf(v_rf_temp, 1e6)
            trap_with_pot_temp.set_bias([0, v_rf_temp + offset, 0, v_rf_temp + offset])
            trap_temp = Trap2D(trap_with_pot_temp)
            trap_temp.set_simulation_parameters(100, 100)
            trap_temp.set_ion(Sr88Ion(), Field2D(side / 2 + 0.4e-3, side / 2 + 0.4e-3), Field2D(400, 400))
            trap_pool.append(trap_temp)

        result = pool.map(run_simulation, trap_pool)
        pool.close()
        pool.join()

        print(map(lambda x: x[1], result).count(True))
    
    trap_with_pot = TrapWithPotential(dim)
    v_rf = 40.0
    trap_with_pot.set_rf(v_rf, 1e6)
    trap_with_pot.set_bias([0, -0.2, 0, -0.2])

    trap = Trap2D(trap_with_pot)
    trap.set_simulation_parameters(100, 100)
    trap.set_ion(Sr88Ion(), Field2D(side / 2 + 0.4e-3, side / 2 + 0.4e-3), Field2D(300, 300))
    trap.start_simulation(False)

    results = trap.results
    t = list(map(lambda x: x[0] * 1000000, results))
    x = list(map(lambda x: x[1].x, results))
    y = list(map(lambda x: x[1].y, results))
    mid = [side / 2] * len(results)
    top = [side - r_rod] * len(results)
    bot = [r_rod] * len(results)
    
    plt.plot(t, x)
    plt.plot(t, y)
    plt.plot(t, mid)
    plt.plot(t, top)
    plt.plot(t, bot)
    plt.show()