import pygame
from queue import PriorityQueue
import math


def distance_pythag(node1, node2): #distance formula
	x1, y1 = node1
	x2, y2 = node2 
	return (((y1 - y2) ** 2) + ((x1-x2) ** 2)) ** .5

def illustrate_path(visitedQueue, curr, draw): 
	while curr in visitedQueue:
		curr = visitedQueue[curr]
		curr.make_path()
		draw()

def a_star(draw, grid, start, end):
	count = 0 
	visitedQueue = {}
	visited_queue = PriorityQueue()
	visited_queue.put((0, count, start))
	g = {node: float("inf") for row in grid for node in row} #g score
	g[start] = 0 
	f = {node: float("inf") for row in grid for node in row} #f score
	f[start] = distance_pythag(start.get_pos(), end.get_pos()) 
	visited_queue_hash = {start}

	while not visited_queue.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		closestChild = visited_queue.get()[2]

		for neighbor in closestChild.neighbors:
			temp_g = g[closestChild]
			if g[neighbor] > temp_g + 1:
				visitedQueue[neighbor] = closestChild
				d = distance_pythag(neighbor.get_pos(), end.get_pos())
				g[neighbor] = temp_g
				f[neighbor] = temp_g + d
				if neighbor not in visited_queue_hash:
					count += 1
					visited_queue.put((f[neighbor], count, neighbor))
					visited_queue_hash.add(neighbor)
					neighbor.make_not_visited()
		if closestChild == end: 
			illustrate_path(visitedQueue, end, draw)
			end.make_end_node()
			start.make_start()
			return True

		draw()

		if closestChild != start:
			closestChild.make_visited()

	return False
