from abc import ABC, abstractmethod

class Simulation(ABC):

    def __init__(self, n_objects):
        self.n_objects = n_objects
        self.static_variables = {}
        self.dynamic_variables = {}

    def set_static(self, variable_name, value):
        if value.shape[0] != self.n_objects:
            raise Exception("Size of the first axis of the 'values' should be equal to the number of objects in the simulation")
        self.static_variables[variable_name] = value
    
    def set_dynamic(self, variable_name, value):
        if value.shape[0] != self.n_objects:
            raise Exception("Size of the first axis of the 'values' should be equal to the number of objects in the simulation")
        self.dynamic_variables[variable_name] = value

    def get_static(self, variable_name, as_list = False):
        static = self.static_variables[variable_name]
        return list(static) if as_list else static

    def get_dynamic(self, variable_name, as_list = False):
        dynamic = self.dynamic_variables[variable_name]
        return list(dynamic) if as_list else dynamic

    def number_of_control_variables(self):
        return sum(
            [dynamic_variable.shape[1] 
            for dynamic_variable in
            self.dynamic_variables.values()]
        )

    def get_dynamic_vars_iterator(self, variables):
        for i in range(self.n_objects):
            yield({dynamic: self.dynamic_variables[dynamic][i] for dynamic in variables})

    @abstractmethod
    def step(self):
        # default behavior of the simulated system. An example
        # is updating the positions when simulating particles
        pass
            
class SimulationUpdater(ABC):

    def __init__(self, simulation: Simulation):
        self.simulation = simulation

    @abstractmethod
    def update(self, deltatime, timestep, signal):
        pass