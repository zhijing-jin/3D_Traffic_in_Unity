# -*- coding: utf-8 -*- 
'''
step1. create a one-pixel route, without intersection of lines
step2. put in the filename, and the codes generate a list of 2D-array storing every point on the route
'''



import numpy as np
import cv2


def display_route(route):
    #route is a list of np.array([pos_i, pos_j])
    import matplotlib.pyplot as plt
    x, y = zip(*route) # unpack data from pairs into x, y
    plt.scatter(x,y) # flip (x,y) into(y,-x)
    plt.show()

def pic_to_pixels(filename):
    im = cv2.imread(filename, 0) # The 0 flag is cv2.CV_LOAD_IMAGE_GRAYSCALE
    
    np.set_printoptions(threshold=1000000)
    print (im)

    point_set = (im <255)
    point_set = zip(list(point_set[0]), list(point_set[1]))
    print(point_set)

    display_route(point_set)
    return point_set
def find_route(point_set):
    # point_set is a 2-D np.array


    #step 1. find the start point
    def find_start_point(point_set):
        for i in range(point_set.shape[0]-1, -1, -1):
            for j in range(point_set.shape[1]):
                if point_set[i][j]:
                    print("start point:", np.array([i,j]))
                    return np.array([i,j])
    #step 2. check adjacents
    def check_next(map, route):
        this_point = route[-1]
        map_shape = np.array(map.shape)
        def adjacents(i=1):
            return  [ 
                        this_point+np.array([i,0]),
                        this_point+np.array([i,i]),                    
                        this_point+np.array([0,i]),
                        this_point+np.array([-i,i]),
                        this_point+np.array([-i,0]),
                        this_point+np.array([-i,-i]),
                        this_point+np.array([0,-i]),
                        this_point+np.array([i,-i])
                        ]
        # i = 1
        # while adjacents(i=i) and i < 8

        for adjacent_point in adjacents(i=1):
            if  ( adjacent_point < map_shape ).all(): # if (adjacent_point < map_shape) is [true, true]
                if map[adjacent_point[0]][adjacent_point[1]] and \
                (adjacent_point != route[-2]).any(): # if they are not exactly same
                    route.append(adjacent_point)
                    return True



    start_point = find_start_point(point_set) # np.array([0,7])
    route = [start_point, start_point] # for the start, we need a useless prev_point
    
    while check_next(point_set, route) :
        pass
    route = route[1:] #delete the first element, which is a placeholder
    print(route)
    
    def route_to_usual_coordinate(route):
        #np.array(img_x, img_y) -> np.array(img_y, 0, -img_x) +offset
        route = np.array(route) # a list of arrays -> an array of arrays(n,2)
        route = np.fliplr(route) * np.array([1, -1]) #np.array(img_x, img_y) -> np.array(img_y, 0, -img_x)
        return route
    route = route_to_usual_coordinate(route)   

    print()
    print(route)


    display_route(route) # an array of arrays(n,2)
    return route




def generate_route():
    filename = "../data/cir.jpg" 
    # filename = "3_example_line.png" 
    point_set = pic_to_pixels(filename)
    route = find_route(point_set) # route: a list of np.array([pos_i, pos_j])
    # this route is after x-y flipping, is consistent with Unity (x,z) coordinate
    outfile = "../data/arbi_traj_2d"
    np.save(outfile, route)
if __name__ == "__main__":
    
	generate_route()
	route = np.load("../data/arbi_traj_2d.npy")

	print()
	print() 
	print(route)
	print("end")