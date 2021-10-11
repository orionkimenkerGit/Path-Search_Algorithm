import pygame
from queue import PriorityQueue
import math

#screen size and caption
height_width = 800
screen = pygame.display.set_mode((height_width, height_width))
pygame.display.set_caption("Path Finding Algorithm Visualizer: A*")

#color variaNbes RGB color code

Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Red = (255, 0, 0)
Black = (0,0,0)
White = (255, 255, 255)
Purple = (128, 0, 128)
Orange = (255, 165, 0)
Teal = (64, 225, 210)
Grey = (128, 128, 128)

#class for each node in the graph
class Node:
	def __init__(self, row, column, side, total_rows):
		self.column = column
		self.row = row 
		self.x = row * side
		self.y = column * side
		self.neighbors = []
		self.side = side
		self.total_rows = total_rows
		self.color = Black

#method that returns position of each node/node
	def get_pos(self):
		return self.row, self.column

#make deach different node type a distinct color
	def make_visited(self):
		self.color = Orange
	def make_not_visited(self):
		self.color = Blue
	def make_wall(self):
		self.color = Grey
	def make_start(self):
		self.color = Yellow
	def make_end_node(self):
		self.color = Purple
	def make_path(self):
		self.color = Teal
#booleans for types of nodes and events based on color
	def visited(self):
		return self.color == Orange
	def not_visited(self):
		return self.color == Blue
	def wall(self):
		return self.color == Grey
	def start_node(self):
		return self.color == Yellow
	def end_node(self):
		return self.color == Purple
	def restart(self):
		self.color = Black 

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.side, self.side))

	#adds neighbors to list 
	def add_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].wall(): #down
			self.neighbors.append(grid[self.row + 1][self.column])
		
		if self.row > 0 and not grid[self.row - 1][self.column].wall(): #up
			self.neighbors.append(grid[self.row - 1][self.column])
		
		if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].wall(): #right
			self.neighbors.append(grid[self.row][self.column + 1])
		
		if self.column > 0 and not grid[self.row][self.column - 1].wall(): #left
			self.neighbors.append(grid[self.row][self.column - 1])

	#to find shortest path diagonally

		if (self.column > 0 and self.row > 0)  and not grid[self.row-1][self.column - 1].wall(): # upper left
			self.neighbors.append(grid[self.row-1][self.column - 1])	

		if (self.row < self.total_rows-1 and self.column >0)  and not grid[self.row+1][self.column - 1].wall(): # upper right
			self.neighbors.append(grid[self.row+1][self.column - 1])	

		if (self.column < self.total_rows-1 and self.row >0)  and not grid[self.row-1][self.column + 1].wall(): # lower left
			self.neighbors.append(grid[self.row-1][self.column + 1])

		if (self.column < self.total_rows-1 and self.row <self.total_rows-1)  and not grid[self.row+1][self.column + 1].wall(): # lower right
			self.neighbors.append(grid[self.row+1][self.column + 1])	
def distance(node1, node2):
	x1, y1 = node1
	x2, y2 = node2 
	return abs(x1-x2) + abs(y1 - y2)

def illustrate_path(prev, curr, draw):
	while curr in prev:
		curr = prev[curr]
		curr.make_path()
		draw()

#main algorithm a*
def a_star(draw, grid, start, end):
	count = 0 
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	prev = {}
	g = {node: float("inf") for row in grid for node in row}
	g[start] = 0
	f = {node: float("inf") for row in grid for node in row}
	f[start] = distance(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		curr = open_set.get()[2]
		#open_set_hash.remove(curr)

		if curr == end: 
			illustrate_path(prev, end, draw)
			end.make_end_node()
			start.make_start()
			return True

		for neighbor in curr.neighbors:
			temp_g = g[curr] + 1 
			if temp_g < g[neighbor]:
				prev[neighbor] = curr
				g[neighbor] = temp_g
				f[neighbor] = temp_g + distance(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_not_visited()
		draw()

		if curr != start:
			curr.make_visited()

	return False


def create_grid(rows, side):
	grid = []
	width = side // rows 
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, width, rows)
			grid[i].append(node)
	return grid

def draw_path(screen, rows, side):
	width = side // rows
	for i in range(rows):
		pygame.draw.line(screen, Teal, (0, i * width), (side, i * width))
		pygame.draw.line(screen, Teal, (i * width, 0), (i * width, side))
def draw(screen, grid, rows, side):
	screen.fill(Black)

	for row in grid:
		for node in row:
			node.draw(screen)
	draw_path(screen, rows, side)
	pygame.display.update()

#helper function to determine what we clicked on
def click_position(position, rows, side):
	width = side // rows 
	y, x = position 
	row = y // width 
	column = x // width 
	return row, column

def main(screen, width):
	ROWS = 40
	grid = create_grid(ROWS, width)
	start = None
	end = None
	run = True
	while run:
		draw(screen, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if pygame.mouse.get_pressed()[0]: #left click
				pos = pygame.mouse.get_pos()
				row, column = click_position(pos, ROWS, width)
				node = grid[row][column]
				if not start and node != end:
					start = node 
					start.make_start()
				elif not end and node != start:
					end = node 
					end.make_end_node()
				elif node != end and node != start:
					node.make_wall()

			elif pygame.mouse.get_pressed()[2]: #right click
				pos = pygame.mouse.get_pos()
				row, column = click_position(pos, ROWS, width)
				node = grid[row][column]
				node.restart()
				if node == start:
					start = None
				elif node == end:
					end = None
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.add_neighbors(grid)

					a_star(lambda: draw(screen, grid, ROWS, width), grid, start, end)
				if event.key == pygame.K_c:
					start = None
					end = None 
					grid = create_grid(ROWS, width)

	pygame.quit()

main(screen, height_width)	