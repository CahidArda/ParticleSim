import turtle
import numpy as np
from time import sleep

HERD_SIZE = 50
DELTATIME = 0.1
SIZE      = 400
SLEEP     = 0.0005
N_ITER    = 100

# turn screen updates off unless 
# wn.update is called
wn = turtle.Screen()
wn.colormode(255)
wn.tracer(0)

def update_screen():
	sleep(SLEEP)
	wn.update()

class Herd:

	def __init__(self, herd_size: int, table_size: int):
		self.herd_size = herd_size
		self.table_size = table_size

		self.xy  = np.random.rand(herd_size, 2)
		self.dxy = np.random.rand(herd_size, 2) - 0.5

		self.colors = np.random.rand(herd_size, 3)
		self.xy_to_color_matrix = (np.random.rand(2,3) - 0.5) * 5

	def update_positions(self, deltatime):
		self.xy += deltatime * self.dxy

		# check_beyond_boundary
		self.dxy[:, 0][self.xy[:, 0] < 0] *= -1
		self.dxy[:, 0][self.xy[:, 0] > 1] *= -1
		self.dxy[:, 1][self.xy[:, 1] < 0] *= -1
		self.dxy[:, 1][self.xy[:, 1] > 1] *= -1

	def update_colors(self):
		self.colors = np.matmul(self.xy, self.xy_to_color_matrix)
		self.colors = 1/(1 + np.exp(-self.colors))

	def list_positions(self):
		return list(self.xy * self.table_size)

	def list_colors(self):
		return list((self.colors * 255).astype(int))
		#return list(self.colors.astype(int))

class Table:

	def __init__(self, size):
		self.size = size
		self.turtles = []

		table_turtle = turtle.Turtle()
		table_turtle.forward(size)
		for _ in range(3):
			table_turtle.left(90)
			table_turtle.forward(size)

	def add_turtle(self, position):
		new_turtle = turtle.Turtle()
		new_turtle.shape('circle')
		new_turtle.penup()
		new_turtle.goto(position)
		self.turtles.append(new_turtle)

	def draw_herd(self, herd: Herd):
		for position in herd.list_positions():
			self.add_turtle(position)
		self.herd = herd
		update_screen()

	def update_herd_colors(self):
		self.herd.update_colors()
		for turtle, color in zip(self.turtles, self.herd.list_colors()):
			turtle.color(*color)

	def update_herd_positions(self, deltatime):
		self.herd.update_positions(deltatime)
		for turtle, position in zip(self.turtles, self.herd.list_positions()):
			turtle.goto(position )

	def table_loop(self, deltatime):
		self.update_herd_positions(deltatime)
		self.update_herd_colors()
		update_screen()



herd  = Herd(HERD_SIZE, SIZE)
table = Table(SIZE)
table.draw_herd(herd)

for _t in range(N_ITER):
	table.table_loop(DELTATIME)

wn.mainloop() 
