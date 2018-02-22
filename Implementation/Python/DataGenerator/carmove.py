import numpy as np
import json
from flask import Flask, jsonify
import requests
from multiprocessing import Process
import sys
from flask import Flask, request

from .global_assignments import *


class Trajectory:
    def __init__(self):
        pass
    def get_travel_time(self, speed):
        pass
    def record_movement(self, interval):
        # cookies is a list of np.array, for UNITY to read
        pass
class Circular_Trajectory(Trajectory):
    
    def __init__(self, center, radius, start_angle, end_angle):
        Trajectory.__init__(self)
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
    def get_travel_time(self, speed):
        angular_speed = speed / self.radius
        time = (self.end_angle-self.start_angle) / angular_speed
        return abs(time)
    def record_movement(self, speed):
        # cookies is a list of np.array, must be a list, for UNITY reading
        

        time = self.get_travel_time(speed)
        cookies_angle = np.linspace(self.start_angle, self.end_angle, num=time)
        cookies = np.column_stack((
                self.radius * np.cos(cookies_angle),
                0*cookies_angle,
                self.radius * np.sin(cookies_angle)
                ))        
        cookies = self.center + cookies
        cookies = cookies.tolist()  # a list of list now
        # print("Circular_Trajectory:", cookies)
        return cookies
class Line_Trajectory(Trajectory):
    def __init__(self, line_start_pos, line_end_pos):
        Trajectory.__init__(self)
        self.line_start_pos = line_start_pos
        self.line_end_pos = line_end_pos
    def get_travel_time(self, speed):
        time = np.linalg.norm(self.line_end_pos - self.line_start_pos)  /  speed
        return abs(time)
    def record_movement(self, speed):
        # cookies is a list of np.array, must be a list, for UNITY reading
        time = self.get_travel_time(speed)
        cookies_x = np.linspace(self.line_start_pos[X_POS], self.line_end_pos[X_POS], num=time)
        cookies_y = np.linspace(self.line_start_pos[Y_POS], self.line_end_pos[Y_POS], num=time)
        cookies_z = np.linspace(self.line_start_pos[Z_POS], self.line_end_pos[Z_POS], num=time)
        cookies = np.column_stack((cookies_x, cookies_y, cookies_z))
        #cookies = cookies.tolist()  # a list of list now
        return cookies
class Arbitrary_Trajectory(Trajectory):
    def __init__(self, ordered_2d_point_set_from_bottom_left, 
        actual_start_pos, actual_end_pos):
        Trajectory.__init__(self)
        # self.ordered_2d_point_set_from_bottom_left: array of arrays, shape(n,2)
        self.ordered_2d_point_set_from_bottom_left = ordered_2d_point_set_from_bottom_left
        self.actual_start_pos = actual_start_pos
        self.actual_end_pos = actual_end_pos

        #np.array(img_x, img_y) -> np.array(img_x, 0, img_y) + offset
        self.ordered_3d_point_set = np.zeros((self.ordered_2d_point_set_from_bottom_left.shape[0], self.ordered_2d_point_set_from_bottom_left.shape[1]+1))
        self.ordered_3d_point_set[:,X_POS] = self.ordered_2d_point_set_from_bottom_left[:,0]
        self.ordered_3d_point_set[:,Z_POS] = self.ordered_2d_point_set_from_bottom_left[:,1]
        scaling_x = np.linalg.norm(self.actual_end_pos[X_POS] - self.actual_start_pos[X_POS])/ \
                    np.linalg.norm(self.ordered_3d_point_set[-1][X_POS] - self.ordered_3d_point_set[0][X_POS])
        scaling_z = np.linalg.norm(self.actual_end_pos[Z_POS] - self.actual_start_pos[Z_POS])/ \
                    np.linalg.norm(self.ordered_3d_point_set[-1][Z_POS] - self.ordered_3d_point_set[0][Z_POS])
        self.ordered_3d_point_set = np.array([scaling_x, 0, scaling_z]) * self.ordered_3d_point_set

        offset = self.actual_start_pos - self.ordered_3d_point_set[0] # offset: a (3,) np.array
        self.ordered_3d_point_set = self.ordered_3d_point_set + offset

    def get_travel_time(self, speed):
        # suppose every two adjacent points is 1 in distance, not sqrt(2)
        time = len(self.ordered_2d_point_set_from_bottom_left) / speed
        return time
    def record_movement(self, speed):        
        time = self.get_travel_time(speed)        
        x = np.linspace(0, self.ordered_3d_point_set.shape[0]-1, num=time) # minus 1: for not indexing the largest boundary
        x = x.astype(int)
        return self.ordered_3d_point_set[x] # a list of [pos_i, pos_j]s


class Car:
    def __init__(self, position):
        self.position = position
    def set_trajectory(self, center, map_size_half, intersection_len_half,
        trajectories):
        
        # self.trajectories = [
        # Line_Trajectory(np.array([0.5,0,-map_size_half]), 
        #     np.array([0.5,0,-intersection_len_half])), 
        # Circular_Trajectory(center, intersection_len_half, 
        #     -np.pi/2, np.pi/2),
        # Line_Trajectory(np.array([0.5,0,intersection_len_half]), 
        #     np.array([0.5,0,map_size_half]))
        # ]
        self.trajectories = trajectories
        # arbi_route = np.load("data/arbi_traj_2d.npy")
        # self.trajectories = [Arbitrary_Trajectory(arbi_route, 
        # np.array([0.5,0,-map_size_half]), np.array([map_size_half,0,0.5]))]
        # # this traj need some amendment because of the offset "0.5"!!
    def movement(self, speed=1):      
        # for the line trajectory
        self.positions = [ i.record_movement(speed)  for i in self.trajectories]
        self.positions = [ i for trajectory in self.positions for i in trajectory] # a list of nparray()
        self.positions = np.array(self.positions)
        # np.save("positions.np", self.positions)
        self.moves = [i-j \
            for i, j in zip(self.positions[:-1], self.positions[1:])]
         
    def export_movement(self, command='toWWW', framerate=1000):
        
        
        data = {}
        for move, pos in zip(self.moves, self.positions[:-1]):
            data["movement"] = nparray_to_vector3(move)
            data["position"] = nparray_to_vector3(pos)
                        

            # print("mv:", data)
            if command == "toWWW":
                export_to_www_json(data)
            elif command == "tofile":
                filename = "car_position_realtime.json"
                filename = "/home/zhi/Downloads/6100/unity/FancyIntersection/Assets/Resources/DataForSettings/VehicleData/cars_realtime_updates.json"
                export_to_json(data, filename)
            
            time.sleep(1.0/framerate) # "speed", by definition, is meter per second

def test_car_movement(trajectories,map_size_half=100, center=np.zeros(3), 
    intersection_len_half=10, lane_width_half=0.5, road_thickness=0.1, 
    num_of_lanes=1 ):

    c = Car(np.array([0.5,0,-map_size_half]))        
    c.set_trajectory(center, map_size_half, intersection_len_half, trajectories)
    c.movement(speed=0.02)
    c.export_movement('toWWW', framerate=1000)









if __name__ == "__main__":
    test_car_movement()
    










            

