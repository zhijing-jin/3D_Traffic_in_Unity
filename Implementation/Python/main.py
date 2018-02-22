from DataGenerator import server, carmove, infrastructure
from multiprocessing import Process
import time
import numpy as np
import argparse
import sys

def p2_set_server_n_send_carmoves(kwargs):
	print("----  setting up server  ----")

	p0 = Process(target=server.launch_server)
	p0.start()

	time.sleep(3)
	print("----  start posting json  ----")

	p1 = Process(target=carmove.test_car_movement, kwargs=kwargs  )
	p1.start()
def send_carmoves(trajectories, kwargs):
	print("----  start posting json  ----")
	carmove.test_car_movement(trajectories, **kwargs)

def set_infrastructure(tofile, kwargs):
	print("----   set infrastructure to file {tofile}  ----".format(tofile=tofile))
	infrastructure.test_infrastructure(tofile=tofile, 
		**kwargs)

if __name__ == "__main__":
	

	kwargs = {"map_size_half":20, "center":np.zeros(3), 
	    "intersection_len_half":20, "lane_width_half":0.5, 
	    "road_thickness":0.1, "num_of_lanes":1 }
	file_infra = '../unity/FancyIntersection/Assets/Resources/DataForSettings/RoadData/lanes.json'
	set_infrastructure(file_infra, kwargs)




	trajectories = [
		carmove.Line_Trajectory(np.array([0.5,0,-kwargs['map_size_half']]), 
            np.array([0.5,0,-kwargs['intersection_len_half']])), 
        carmove.Circular_Trajectory(kwargs['center'], kwargs['intersection_len_half'], 
            -np.pi/2, np.pi/2),
        carmove.Line_Trajectory(np.array([0.5,0,kwargs['intersection_len_half']]), 
	        np.array([0.5,0,kwargs['map_size_half']]))
	]
	trajectories = trajectories[1:2]
	# for an arbitrary traj:
	# arbi_route = np.load("./data/arbi_traj_2d.npy")
	# trajectories = [carmove.Arbitrary_Trajectory(arbi_route, \
	# 	np.array([0.5,0,-kwargs['map_size_half']]), np.array([kwargs['map_size_half'],0,0.5]))]
	send_carmoves(trajectories, kwargs)
	
	
	
