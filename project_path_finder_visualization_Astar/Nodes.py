import pygame

#colors
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
	def redo(self):
		self.color = Black 
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



	#method that returns position of each node/node
	def get_pos(self):
		return self.row, self.column


	def draw(self, screen):
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.side, self.side))

	#adds neighbors to list 
	def add_neighbors(self, grid): #finds neighbors of each node i.e. the nodes that aren't already walls
		self.neighbors = []

		if (self.column > 0) and not grid[self.row][self.column - 1].wall(): #left
			self.neighbors.append(grid[self.row][self.column - 1])

		if (self.column < (self.total_rows - 1)) and not grid[self.row][self.column + 1].wall(): #right
			self.neighbors.append(grid[self.row][self.column + 1])
		
		if (self.row > 0) and not grid[self.row - 1][self.column].wall(): #up
			self.neighbors.append(grid[self.row - 1][self.column])

		if (self.row < (self.total_rows - 1)) and not grid[self.row + 1][self.column].wall(): #down
			self.neighbors.append(grid[self.row + 1][self.column])

	#to find shortest path diagonally, finds diagonal neighbors of each node

		if (self.column > 0 and self.row > 0)  and not grid[self.row -  1][self.column - 1].wall(): # upper left
			self.neighbors.append(grid[self.row - 1][self.column - 1])	

		if (self.row < (self.total_rows - 1)) and self.column > 0  and not grid[self.row + 1][self.column - 1].wall(): # upper right
			self.neighbors.append(grid[self.row + 1][self.column - 1])	

		if (self.column < (self.total_rows - 1)) and self.row > 0  and not grid[self.row - 1][self.column + 1].wall(): # lower left
			self.neighbors.append(grid[self.row - 1][self.column + 1])

		if (self.column < (self.total_rows - 1)) and (self.row < (self.total_rows - 1)) and not grid[self.row + 1][self.column + 1].wall(): # lower right
			self.neighbors.append(grid[self.row + 1][self.column + 1])	