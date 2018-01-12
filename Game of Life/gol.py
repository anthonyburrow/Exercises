import Tkinter as tk
from Tkinter import *
from threading import Timer
import math

####### SETTINGS #######

interval = 0.3					# Seconds for each refresh
width = 40						# Number of columns
height = 40						# Number of rows

window_width = 700				# Window width in px
window_height = 700				# Window height in px (not counting control button)

live_color = "#424242"			# Color of living cells
dead_color = "#bababa"			# Color of dead cells

button_border_width = 1			# Cell border width in px

########################

class Controller:

	# Initialize

	def __init__(self, _interval, _live_color, _dead_color):
		self._interval = _interval
		self._live_color = _live_color
		self._dead_color = _dead_color

		self.populate_timer = None
		self.is_running = False

		self.buttons = []
		self.alive = []

	# Function to manage iterations

	def _run(self):
		self.is_running = self.populate()
		if self.is_running: #repeat if there are still cells, or if stop() or clear() is called
			self.start()

	# Function to begin iterations

	def start(self):
		iter_button.configure(text = "Stop", command=lambda: self.stop())

		self.is_running = True
		self.populate_timer = Timer(self._interval, self._run)
		self.populate_timer.start()

	# Function to stop populating

	def stop(self):
		self.populate_timer.cancel()
		self.is_running = False

		iter_button.configure(text = "Start", command=lambda: self.start())

	# Function to clear grid and stop populating

	def clear(self):
		if self.is_running:
			self.stop()

		for coord in self.alive:
			button = self.buttons[coord[0]][coord[1]]
			button.configure(bg = self._dead_color)

		self.alive = []

	# Function to change color when a cell is clicked

	def click(self, row, col):
		"""
		Parameters:
		==========
		row: row of cell being clicked
		col: column of cell being clicked
		"""

		button = self.buttons[row][col]
		coord = [row, col]

		if coord not in self.alive:
			button.configure(bg = self._live_color)
			self.alive.append(coord)
		elif coord in self.alive:
			button.configure(bg = self._dead_color)
			self.alive.remove(coord)

	# Function that updates each cell during each refresh cycle

	def populate(self):

		if self.alive:
			#Reset for each time it repopulates
			dead_neighbors_checked = []
			turn_alive = []
			turn_dead = []

			for coord in self.alive:
				row = coord[0]
				col = coord[1]
				neighbors = self.check_neighbors(row, col, dead_neighbors_checked, turn_alive)

				#RULE 1
				if neighbors < 2:
					turn_dead.append(coord)
				#RULE 2
				elif (neighbors == 2) or (neighbors == 3):
					pass
				#RULE 3
				elif neighbors > 3:
					turn_dead.append(coord)

			for coord in turn_alive:
				row = coord[0]
				col = coord[1]
				button = self.buttons[row][col]
				button.configure(bg = self._live_color)
				self.alive.append(coord)

			for coord in turn_dead:
				row = coord[0]
				col = coord[1]
				button = self.buttons[row][col]
				button.configure(bg = self._dead_color)
				self.alive.remove(coord)

			return True

		else:
			print "There are no living cells."
			iter_button.configure(text = "Start", command=lambda: self.start())
			return False

	# Function that checks how many neighbors a cell has

	def check_neighbors(self, r, c, _dead_neighbors_checked, _turn_alive):
		"""
		Parameters:
		==========
		r: row of cell to check
		c: column of cell to check
		_dead_neighbors_checked: memoization list carried from populate() of surrounding dead cells 
		_turn_alive: list given by populate() to check for those cells to become alive
		"""

		live_neighbors = []
		for i in [-1,0,1]:
			for j in [-1,0,1]:
				coo = [r + i, c + j]

				if (i != 0 or j != 0) and (coo in self.alive):
					live_neighbors.append(coo)

				if (i != 0 or j != 0) and (coo not in self.alive) and (coo not in _dead_neighbors_checked):
					_dead_neighbors_checked.append(coo)

					live_neighbors_of_dead = []
					for m in [-1,0,1]:
						for n in [-1,0,1]:
							deadcoo = [coo[0] + m, coo[1] + n]
							if (m != 0 or n != 0) and (deadcoo in self.alive):
								live_neighbors_of_dead.append(deadcoo)
					num = len(live_neighbors_of_dead)

					#RULE 4
					if num == 3:
						_turn_alive.append(coo)

		return len(live_neighbors)

# Setup GUI

root = tk.Tk()
button_container = tk.Frame(root)
button_container.grid(row = height + 1, columnspan = width, sticky = "wens", padx = 6, pady = 6)

blank_image = tk.PhotoImage()
button_width = math.ceil(window_width/width)
button_height = math.ceil(window_height/height)

# Create object and setup initial state

controller = Controller(interval, live_color, dead_color)

for row in range(height):
	controller.buttons.append([])
	for col in range(width):
		button = tk.Button(root, width = button_width, height = button_height, 
						    bg = dead_color, image = blank_image, borderwidth = button_border_width,
                           command=lambda row=row, col=col: controller.click(row, col))
		controller.buttons[row].append(button)
		button.grid(row=row, column=col, sticky="nsew")

iter_button = tk.Button(button_container, text = "Start",
						command=lambda: controller.start())
iter_button.pack(fill = BOTH, expand = True, side = LEFT)

clear_button = tk.Button(button_container, text = "Clear",
						command=lambda: controller.clear())
clear_button.pack(fill = BOTH, expand = True, side = RIGHT)

root.mainloop()