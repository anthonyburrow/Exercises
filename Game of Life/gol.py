import Tkinter as tk
from Tkinter import *
from threading import Timer
import math

#######SETTINGS#######

speed = 0.3						# Seconds for each refresh
width = 40						# Number of columns
height = 40						# Number of rows

window_width = 700				# Window width in px
window_height = 700				# Window height in px (not counting control button)

live_color = "#424242"			# Color of living cells
dead_color = "#bababa"			# Color of dead cells

######################

root = tk.Tk()
button_container = tk.Frame(root)
button_container.grid(row = height + 1, columnspan=width, sticky="wens", padx = 6, pady = 6)
buttons = []
alive = []
is_running = False
is_clearing = False

dead_neighbors_checked = [] #compilation & writing purposes
turn_alive = []
turn_dead = []

#Function to change color when a cell is clicked

def click(row, col):
	button = buttons[row][col]
	coord = [row, col]

	if coord not in alive:
		button.configure(bg = live_color)
		alive.append(coord)
	elif coord in alive:
		button.configure(bg = dead_color)
		alive.remove(coord)

#Function to clear grid

def clear():
	global dead_neighbors_checked
	global turn_alive
	global turn_dead
	global alive
	dead_neighbors_checked = []
	turn_alive = []
	turn_dead = []
	
	for coord in alive:
		button = buttons[coord[0]][coord[1]]
		button.configure(bg = dead_color)
	alive = []

	is_clearing = False

def clearing_timer():
	global is_clearing
	is_clearing = True
	t = Timer(speed, clear())
	t.start()

#Functions that implement the game mechanics

def check_neighbors(r, c):
	live_neighbors = []
	global dead_neighbors_checked
	global turn_alive

	for i in [-1,0,1]:
		for j in [-1,0,1]:
			coo = [r + i, c + j]

			if (i != 0 or j != 0) and (coo in alive):
				live_neighbors.append(coo)

			if (i != 0 or j != 0) and (coo not in alive) and (coo not in dead_neighbors_checked):
				dead_neighbors_checked.append(coo)

				live_neighbors_of_dead = []
				for m in [-1,0,1]:
					for n in [-1,0,1]:
						deadcoo = [coo[0] + m, coo[1] + n]
						if (m != 0 or n != 0) and (deadcoo in alive):
							live_neighbors_of_dead.append(deadcoo)
				num = len(live_neighbors_of_dead)

				#RULE 4
				if num == 3:
					turn_alive.append(coo)

	return len(live_neighbors)

def populate():
	if alive: #if there are any alive
		global dead_neighbors_checked
		global turn_alive
		global turn_dead
		dead_neighbors_checked = [] #Reset for each time it repopulates
		turn_alive = []
		turn_dead = []

		for coord in alive:
			row = coord[0]
			col = coord[1]
			neighbors = check_neighbors(row, col)

			#RULE 1
			if neighbors < 2:
				turn_dead.append(coord)
			#RULE 2
			elif (neighbors == 2) or (neighbors == 3):
				pass
			#RULE 3
			elif neighbors > 3:
				turn_dead.append(coord)

		if not is_clearing:
			for coord in turn_alive:
				row = coord[0]
				col = coord[1]
				button = buttons[row][col]
				button.configure(bg = live_color)
				alive.append(coord)

			for coord in turn_dead:
				row = coord[0]
				col = coord[1]
				button = buttons[row][col]
				button.configure(bg = dead_color)
				alive.remove(coord)

	else:
		print "There are no living cells."

		global is_running
		is_running = False

		iter_button.configure(text = "Start", command=lambda: IterateController(speed))

#Start and stop timer controller

class IterateController:
	
	def __init__(self, interval):
		self._timer = None
		self.interval = interval
		self.start()

	def _run(self):
		populate()
		global is_clearing
		if is_running and not is_clearing:
			self.start()

	def start(self):
		global is_running

		iter_button.configure(text = "Stop", command=lambda: self.stop())


		is_running = True
		self._timer = Timer(self.interval, self._run)
		self._timer.start()

	def stop(self):
		self._timer.cancel()
		is_running = False

		iter_button.configure(text = "Start", command=lambda: self.start())


#Setup initial state

blank_image = tk.PhotoImage()
button_width = math.ceil(window_width/width)
button_height = math.ceil(window_height/height)

for row in range(height):
	buttons.append([])
	for col in range(width):
		button = tk.Button(root, width = button_width, height = button_height, 
						    bg = dead_color, image = blank_image, borderwidth = 1,
                           command=lambda row=row, col=col: click(row, col))
		buttons[row].append(button)
		button.grid(row=row, column=col, sticky="nsew")

iter_button = tk.Button(button_container, text = "Start",
						command=lambda: IterateController(speed))
iter_button.pack(fill = BOTH, expand = True, side = LEFT)

clear_button = tk.Button(button_container, text = "Clear",
						command=lambda: clear())
clear_button.pack(fill = BOTH, expand = True, side = RIGHT)


root.mainloop()