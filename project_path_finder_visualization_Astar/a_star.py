import pygame
from queue import PriorityQueue
import math


def distance_pythag(node1, node2): #distance formula
	x1, y1 = node1
	x2, y2 = node2 
	return (((y1 - y2) ** 2) + ((x1-x2) ** 2)) ** .5

def illustrate_path(closed_set, curr, draw): 
	while curr in closed_set:
		curr = closed_set[curr]
		curr.make_path()
		draw()


def a_star(draw, grid, start, end):


	count = 0 
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	closed_set = {}
	g = {node: float("inf") for row in grid for node in row}
	g[start] = 0
	f = {node: float("inf") for row in grid for node in row}
	f[start] = distance_pythag(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		curr = open_set.get()[2]
		#open_set_hash.remove(curr)

		if curr == end: 
			illustrate_path(closed_set, end, draw)
			end.make_end_node()
			start.make_start()
			return True

		for neighbor in curr.neighbors:
			temp_g = g[curr] + 1 
			if temp_g < g[neighbor]:
				closed_set[neighbor] = curr
				g[neighbor] = temp_g
				f[neighbor] = temp_g + distance_pythag(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_not_visited()
		draw()

		if curr != start:
			curr.make_visited()

	return False

