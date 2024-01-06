import numpy as np

from simpy import *

## CONFIG ##

N_PARTICLES = 100

DRAWING_SIZE = 400

N_STEPS   = 1000
DELTATIME = 0.1
SLEEP     = 0.00001

## CONFIG ##

class ParticleSimulation(Simulation):
    # holds the particles and their information
    def __init__(self, n_particles: int):
        super().__init__(n_particles)
        self.set_dynamic('xy', np.random.rand(n_particles, 2))
        self.set_dynamic('dxy', np.random.rand(n_particles, 2) - 0.5)
        self.set_dynamic('size', np.ones((n_particles, 1)))
        self.set_dynamic('color', np.ones((n_particles, 3)))

    def step(self, deltatime: float):
        xy = self.get_dynamic('xy')
        dxy = self.get_dynamic('dxy')
        xy += deltatime * dxy

        # check_beyond_boundary
        dxy[:, 0][xy[:, 0] < 0] *= -1
        dxy[:, 0][xy[:, 0] > 1] *= -1
        dxy[:, 1][xy[:, 1] < 0] *= -1
        dxy[:, 1][xy[:, 1] > 1] *= -1
        
        self.set_dynamic('xy', xy)
        self.set_dynamic('dxy', dxy)

class ParticleUpdater(SimulationUpdater):
    # updates particles based on some rule using a sigal as input
    def __init__(self, particles_simulation: Simulation):
        super().__init__(particles_simulation)
        self.color_mat_1 = (np.random.rand(2,3) - 0.5) * 5
        self.color_mat_2 = (np.random.rand(2,3) - 0.5) * 5
        self.size_mat    = np.random.rand(2,1)

    def set_positional_color(self, signal):

        def get_color(xy, mat, signal):
            colors = np.matmul(xy, mat)
            colors = 1/(1 + np.exp(-colors))
            colors *= signal
            return colors

        xy = self.simulation.get_dynamic('xy')
        color_1 = get_color(xy, self.color_mat_1, signal)
        color_2 = get_color(xy, self.color_mat_2, 1-signal)
        
        colors = color_1 + color_2       
        colors = (colors * 255).astype(int)
        self.simulation.set_dynamic('color', colors)

    def set_positional_size(self):
        size = np.matmul(self.simulation.get_dynamic('xy'), self.size_mat)
        size = 1/(1 + np.exp(-size))
        self.simulation.set_dynamic('size', size)

    def set_xy_and_time_dependent_size(self, timestep):
        total_distance = np.sum(self.simulation.get_dynamic('xy'), axis = 1)
        size = np.sin(total_distance + timestep / 10)
        self.simulation.set_dynamic('size', size)

    def set_signal_based_energy(self, signal):
        speeds = self.simulation.get_dynamic('dxy')
        normal_speeds = speeds / sum(np.abs(speeds))
        self.simulation.set_dynamic('dxy', normal_speeds * (signal + 0.5))

    def update(self, deltatime, timestep, signal):
        self.set_positional_color(signal)
        self.set_signal_based_energy(signal)
        self.set_xy_and_time_dependent_size(timestep)



import turtle
from time import sleep

# turn screen updates off unless 
# wn.update is called
wn = turtle.Screen()
wn.colormode(255)
wn.tracer(0)

def update_screen():
	sleep(SLEEP)
	wn.update()

class ParticleDrawer:
    def __init__(self, size: int, simulation: Simulation):
        self.size = size
        self.simulation = simulation

        # draw boundary
        table_turtle = turtle.Turtle()
        table_turtle.forward(size)
        for _ in range(3):
            table_turtle.left(90)
            table_turtle.forward(size)

        # draw turtles
        self.turtles = []
        for xy in simulation.get_dynamic('xy', as_list=True):
            self.add_turtle(xy * self.size)

    def add_turtle(self, position):
        new_turtle = turtle.Turtle()
        new_turtle.shape('circle')
        new_turtle.penup()
        new_turtle.goto(position)
        self.turtles.append(new_turtle)
        
    def refresh(self):
        for turtle, kwargs in zip(self.turtles, self.simulation.get_dynamic_vars_iterator(['xy', 'size', 'color'])):
            turtle.goto(kwargs['xy'] * self.size)
            turtle.color(kwargs['color'])
            turtle.shapesize(kwargs['size'])

sim = ParticleSimulation(N_PARTICLES)
updater = ParticleUpdater(sim)
drawer  = ParticleDrawer(DRAWING_SIZE, sim)

signal = np.sin(np.arange(N_STEPS) / 5) * 0.5 + 0.5
for timestep, signal_i in zip(range(N_STEPS), signal):
    updater.update(DELTATIME, timestep, signal_i)
    sim.step(DELTATIME)

    drawer.refresh()
    update_screen()
    