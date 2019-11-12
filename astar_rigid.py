import numpy as np
import matplotlib.pyplot as plt
import math
from heapq import *
import sys

def create_graph(clearance, radius): 
	graph = {}
	for i in range(250):
		for j in range(150):
			circle = ((i - 190) ** 2 + (j - 130)**2 - (15 ** 2))
			ellipse = (((i - 140) / 15) ** 2 + ((j - 120) / 6) ** 2) - 1

			aug_circle = ((i - 190) ** 2 + (j - 130)**2 - ((15+clearance+radius) ** 2))
			aug_ellipse = (((i - 140) / (15+clearance+radius)) ** 2 + ((j - 120) / (6+clearance+radius)) ** 2) - 1

			h1 = 50 - i
			h2 = i - 100
			h3 = j - 112.5
			h4 = 67.5 -j

			aug_h1 = 50 - (i+clearance+radius)
			aug_h2 = (i-clearance-radius) - 100
			aug_h3 = (j-clearance-radius) - 112.5
			aug_h4 = 67.5 -(j+clearance+radius)

			p1 = (j-56) + 1.64*(i - 125)
			p2 = j - 15
			p3 = (j - 15) - 1.85*(i-173)
			p4 = (j-90) + 1.65*(i-170)
			p5 = (j-90) - 5.42*(i-170)
			p6 = (j-56) + 0.10*(i-125)
			p7 = (j -15) -2.84*(i - 150)
			p8 = j - 52

			aug_p1 = (j-56) + 1.64*(i - 125) +(radius+clearance)*math.sqrt(1+(1.64**2))
			aug_p2 = j - 15 + radius + clearance
			aug_p3 = (j - 15) - 1.85*(i-173)+(radius+clearance)*math.sqrt(1+(1.85**2))
			aug_p4 = (j-90) + 1.65*(i-170)-(radius+clearance)*math.sqrt(1+(1.65**2))
			aug_p5 = (j-90) - 5.42*(i-170)-(radius+clearance)*math.sqrt(1+(5.42**2))
			aug_p6 = (j-56) + 0.10*(i-125)-(radius+clearance)*math.sqrt(1+(0.10**2))
			aug_p7 = (j -15) -2.84*(i - 150)-(radius+clearance)*math.sqrt(1+(2.84**2))
			aug_p8 = j - 52 -radius-clearance

			graph[(i,j)] = {'visited':False, 'distance':np.inf, 'valid':True, 'parent': (0, 0), 'id':'blank'}
			if circle <= 0:
				graph[(i,j)]['valid'] = False
				graph[(i,j)]['id'] = 'obs'
			elif aug_circle <=0:
				graph[(i,j)]['valid'] = False
				graph[(i,j)]['id'] = 'aug'
			if ellipse <= 0:
				graph[(i,j)]['valid'] = False
				graph[(i,j)]['id'] = 'obs'
			elif aug_ellipse <=0:
				graph[(i,j)]['valid'] = False
				graph[(i,j)]['id'] = 'aug'
			if h1 <= 0 and h2 <= 0 and h3 <=0 and h4 <=0:
				graph[(i,j)]['valid'] = False
				graph[(i,j)]['id'] = 'obs'
			elif aug_h1 <= 0 and aug_h2 <= 0 and aug_h3 <=0 and aug_h4 <=0:
				graph[(i,j)]['valid'] = False
				graph[(i,j)]['id'] = 'aug'
			elif p1 >=0 and p2 >=0 and p6 <=0 and p7 >=0:
				graph[(i,j)]['valid'] = False
				graph[(i,j)]['id'] = 'obs'
			elif aug_p1 >=0 and aug_p2 >=0 and aug_p6 <=0 and aug_p7 >=0:
				graph[(i,j)]['valid'] = False
				graph[(i,j)]['id'] = 'aug'
			elif p4 <=0 and p5 <=0 and p8 >=0:
				graph[(i,j)]['valid'] = False
				graph[(i,j)]['id'] = 'obs'
			elif aug_p4 <=0 and aug_p5 <=0 and aug_p8 >=0:
				graph[(i,j)]['valid'] = False
				graph[(i,j)]['id'] = 'aug'
			elif p2 >=0 and p3 >= 0 and p7 <=0 and p8 <=0:
				graph[(i,j)]['valid'] = False
				graph[(i,j)]['id'] = 'obs'
			elif aug_p2 >=0 and aug_p3 >= 0 and aug_p7 <=0 and aug_p8 <=0:
				graph[(i,j)]['valid'] = False
				graph[(i,j)]['id'] = 'aug'
	return graph


def astar(graph, source, goal):
	count = 0
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

	clearance = int(input("Enter clearance: "))
	radius = int(input("Enter robot radius: "))
	g = create_graph(clearance, radius)
	#grid_size = input("Enter grid_size: ")

	points = [x for x in g.keys() if not (g[x]['valid'])]

	# if x1,y1 in points or p,q in points:
	#     print("Start or goal state inside the obstacle, exiting")
	#     return
	x = [i[0] for i in points]
	y = [i[1] for i in points]
	for i in points:
		if x1 == i[0] and y1 == i[1]:
			print("Start point inside obstacle, exiting")
			sys.exit(0)
		if p == i[0] and q == i[1]:
			print("Goal point inside obstacle, exiting")
			sys.exit(0)
	
	obs_points = [x for x in g.keys() if (g[x]['id']) == 'obs']
	obs_x = [i[0] for i in obs_points]
	obs_y = [i[1] for i in obs_points]

	aug_points = [x for x in g.keys() if (g[x]['id']) == 'aug']
	aug_x = [i[0] for i in aug_points]
	aug_y = [i[1] for i in aug_points]

	plt.xlim(right=250)
	plt.ylim(top=150)
	plt.plot(obs_x,obs_y, 'k.')
	plt.plot(aug_x,aug_y, 'r.')
	plt.plot(x1,y1,'Xb')
	plt.plot(p,q,'Xg')
	min_distance, path = astar(g, start, goal)
	#print("Minimum Distance from start to goal:", min_distance)
	x = [i[0] for i in path]
	y = [i[1] for i in path]
	plt.plot(x,y, 'g-')
	plt.show()