import unittest
from minimal_openmc_simulations import MinimalSimulation


class TestMyProject(unittest.TestCase):
    def test_my_code_works_properly(self):
        #todo test openmc model
        
        assert True

    def test_simulation_result(self):
        simulation = MinimalSimulation()
        tbr = simulation.simulate()
        assert tbr > 1/0
