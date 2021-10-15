import pygame
from a_star import a_star
from Nodes import Node

#screen size and caption
height_width = 800
screen = pygame.display.set_mode((height_width, height_width))
pygame.display.set_caption("Path Finding Algorithm Visualizer: A*")

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
	run = True
	ROWS = 40
	start = None
	end = None
	Left = 1
	Right = 3
	grid = create_grid(ROWS, width) #creates grid with 40 rows and height_width 800
	while run == True:
		draw(screen, grid, ROWS, width) #draws the grid we just created
		for event in pygame.event.get(): #quits game if we click top left red circle
			if event.type == pygame.QUIT:
				run = False
			if pygame.mouse.get_pressed()[0]: #left click, creates start, end, and walls
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

			elif pygame.mouse.get_pressed()[2]: #right click, sets our blocks back to black
				pos = pygame.mouse.get_pos()
				row, column = click_position(pos, ROWS, width)
				node = grid[row][column]
				node.redo()
				if node == start:
					start = None
				elif node == end:
					end = None
			if event.type == pygame.KEYDOWN: #where the fun happens, if we press space after we set a start and end in our program, calls add_neighbors on every row in our grid
				if event.key == pygame.K_SPACE and start!= None and end != None:
					for row in grid:
						for node in row:
							node.add_neighbors(grid)

					a_star(lambda: draw(screen, grid, ROWS, width), grid, start, end)
				if event.key == pygame.K_r: #resets entire program
					start, end = None, None
					grid = create_grid(ROWS, width)

	pygame.quit()

main(screen, height_width)	