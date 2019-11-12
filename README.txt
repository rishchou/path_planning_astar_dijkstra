# Submitted by: Rishabh Choudhary
# UID: 116348768

## Instructions to Run the project

There are 4 files in this directory:
1. dijkstra_point py - Dijkstra for point robot
2. astar_point.py  - Astar for point robot
3. dijkstra_rigid.py - Dijkstra for rigid robot
4. astar_rigid.py - Astar for rigid robot


These files have been tested with python3.

To run any of these files, run them as follows:

"python3 <filename>.py"

After running using above command, the animation window will open up showing visited nodes and obstacle space.
After maximizing the terminal window,output path will be drawn when goal is reached.


File 1 and 2 have two input arguments, start and goal point. 
The value of x and y should lie between 0 <= x <= 249 and 0<=y<=149
Input start and goal state in the form of x and y coordinates with a space between them.
Invalid arguments will make the code exit.

File 3 and 4 have extra input parameters of clearance and robot radius. Input them as normal integers to expand the obstacle space.

Assumptions:

-> The map is of size (250x150)
-> The unit grid size is of 1.
-> Points outside the map or within the obstacle will return error and make the code exit.
