import numpy as np
import matplotlib.pyplot as plt
import math
from heapq import *
import sys

def create_graph(): 
	graph = {}
	
	for i in range(250):
		for j in range(150):
			# Equation of circle
			circle = ((i - 190) ** 2 + (j - 130)**2 - (15 ** 2))
			# Equation of ellipse
			ellipse = (((i - 140) / 15) ** 2 + ((j - 120) / 6) ** 2) - 1
			# Rectangle half plane equations
			h1 = 50 - i
			h2 = i - 100
			h3 = j - 112.5
			h4 = 67.5 -j
			#Polygon half plane equations
			p1 = (j-56) + 1.64*(i - 125)
			p2 = j - 15
			p3 = (j - 15) - 1.85*(i-173)
			p4 = (j-90) + 1.65*(i-170)
			p5 = (j-90) - 5.42*(i-170)
			p6 = (j-56) + 0.10*(i-125)
			p7 = (j -15) -2.84*(i - 150)
			p8 = j - 52

			graph[(i,j)] = {'visited':False, 'distance':np.inf, 'valid':True, 'parent': (0, 0)}
			if circle <= 0:
				graph[(i,j)]['valid'] = False
			if ellipse <= 0:
				graph[(i,j)]['valid'] = False
			if h1 <= 0 and h2 <= 0 and h3 <=0 and h4 <=0:
				graph[(i,j)]['valid'] = False
			if p1 >=0 and p2 >=0 and p6 <=0 and p7 >=0:
				graph[(i,j)]['valid'] = False
			if p4 <=0 and p5 <=0 and p8 >=0:
				graph[(i,j)]['valid'] = False
			if p2 >=0 and p3 >= 0 and p7 <=0 and p8 <=0:
				graph[(i,j)]['valid'] = False
	return graph

def astar(graph, source, goal):
	row = []
	(goal_x, goal_y) = goal
	graph[source]['visited'] = True
	num_nodes_visited = 1
	graph[source]['distance'] = 0
	queue = []
	queue_distance = calculate_distance(goal, source)+graph[source]['distance']
	heappush(queue, (queue_distance, source))
	while (len(queue) != 0):
		current = heappop(queue)[1]
		if current == goal:
			print("Goal reached")
			if row:
				x,y = zip(*row)
				plt.plot(x,y,'y.')
				plt.pause(0.01)
			break
		for i in [-1, 0, 1]:
			for j in [-1, 0, 1]:
				if i != 0 or j != 0:
					neighbour = (abs(current[0]+i), abs(current[1]+j))
					lst = list(neighbour)
					if lst[0] >=250:
						lst[0] = 249
					if lst[1] >=150:
						lst[1] = 149
					neighbour = tuple(lst)
					if graph[neighbour]['valid'] == True:

						if abs(i)+abs(j) == 2:
							distance = math.sqrt(2)
						else:
							distance = 1

						if graph[neighbour]['visited'] == False:
							graph[neighbour]['visited'] = True
							row.append([abs(current[0]+i), abs(current[1]+j)])
							x,y = zip(*row)
							if num_nodes_visited %50 == 0:
								plt.plot(x,y,'y.')
								row.clear()
								plt.pause(0.01)
								
							num_nodes_visited += 1							
							graph[neighbour]['parent'] = current								
							graph[neighbour]['distance'] = graph[current]['distance'] + distance
							queue_distance = calculate_distance(goal, neighbour)+graph[neighbour]['distance']
							heappush(queue, (queue_distance, neighbour))
							                                  	
	path = [(goal_x, goal_y)]
	parent = (goal_x, goal_y)
	while parent != source:
		parent = graph[path[len(path)-1]]['parent']
		path.append(parent)
	min_distance = (graph[(goal_x,goal_y)]['distance'])	
	print("Total Number of Nodes Visited:", num_nodes_visited)  	
	return(min_distance, path)

def calculate_distance(goal, current):
	d = math.sqrt(((goal[0]-current[0])*(goal[0]-current[0]))+((goal[1]-current[1])*(goal[1]-current[1])))
	return d

if __name__ == "__main__":
	
	x1,y1 = input("Enter start point, with a space between x and y coordinates of start ").split()
	x1 = int(x1)
	y1 = int(y1)
	start = (x1,y1)
	if x1 >= 250 or x1 < 0 or y1 >= 150 or y1 <0:
		print("Invalid start state, exiting")
		sys.exit(0)
	p,q = input("Enter goal point, with a space between x and y coordinates of goal: ").split()
	p = int(p)
	q = int(q)
	goal = (p,q)
	if p >= 250 or p < 0 or q >= 150 or q <0:
		print("Invalid Goal state, exiting")
		sys.exit(0)

	g = create_graph()

	points = [x for x in g.keys() if not (g[x]['valid'])]

	x = [i[0] for i in points]
	y = [i[1] for i in points]
	for i in points:
		if x1 == i[0] and y1 == i[1]:
			print("Start point inside obstacle, exiting")
			sys.exit(0)
		if p == i[0] and q == i[1]:
			print("Goal point inside obstacle, exiting")
			sys.exit(0)
	
	plt.xlim(right=250)
	plt.ylim(top=150)	
	plt.plot(x,y, 'k.')
	plt.plot(x1,y1,'Xr')
	plt.plot(p,q,'Xg') 
	min_distance, path = astar(g, start, goal)
	#print("Minimum Distance from start to goal:", min_distance)
	x = [i[0] for i in path]
	y = [i[1] for i in path]
	plt.plot(x,y, 'g-')
	plt.show()