import numpy as np
import json
from flask import Flask, jsonify
import requests
from multiprocessing import Process
import sys
import time
from flask import Flask, request



X_POS , Y_POS, Z_POS = 0, 1, 2
def nparray_to_vector3(arr):
    return { "x": arr[X_POS],
            "y": arr[Y_POS],
            "z": arr[Z_POS]
            }
def export_to_json(obj, filename):    
    with open(filename, 'w') as fout:
        json.dump(obj, fout, indent=4)
        '''
        jsoned_data = json.dumps(oldData, indent=True)
        json_file.write(jsoned_data)
        '''


def export_to_www_json(obj, url='http://127.0.0.1:5000'):
    r = requests.post(url, data=json.dumps(obj))
    

class Leg:
    def __init__(self, leg_center, leg_length, direction_from_center):
        self.leg_center = leg_center
        self.leg_length = leg_length
        self.direction_from_center = direction_from_center # 0,1,2,3 => x+, z+, x-, z-
class Lane:
    def __init__(self, position, scale, traffic_direction):
        self.position = position
        self.scale = scale
        self.traffic_direction = traffic_direction

        # transform np.array of (3,) into Vector3 for Unity 
        self.position = {"x": position[X_POS],
                            "y": position[Y_POS],
                            "z": position[Z_POS]}
        self.scale = {"x": scale[X_POS],
                      "y": scale[Y_POS],
                      "z": scale[Z_POS]}
    def __repr__(self): # for printing out the class as a string
        return str(self.__dict__)
class Intersection:
    def __init__(self, center, intersection_len_half):
        self.position = {"x": center[X_POS],
                        "y": center[Y_POS],
                        "z": center[Z_POS]}
        self.scale = {"x": 2*intersection_len_half,
                    "y": 0,
                    "z": 2*intersection_len_half}
                        

class Construct_legs:
    def __init__(self, map_size_half=100, center=np.zeros(3), intersection_len_half=10,
        lane_width_half=0.5, road_thickness=0.1, num_of_lanes=1):
        self.map_size_half = map_size_half
        self.center = center
        self.intersection_len_half = intersection_len_half
        self.lane_width_half = lane_width_half
        self.road_thickness = road_thickness
        self.num_of_lanes = num_of_lanes
    
    def construct_legs(self):
        
        leg_centers = np.tile(self.center, (4,1)) # turn [a,b,c] into [[a,b,c],[a,b,c],[a,b,c],[a,b,c]]
        center_to_leg_center_distance = (self.intersection_len_half + self.map_size_half)/2
        
        leg_centers[0][X_POS] = leg_centers[0][X_POS] + center_to_leg_center_distance
        leg_centers[1][Z_POS] = leg_centers[1][Z_POS] + center_to_leg_center_distance
        leg_centers[2][X_POS] = leg_centers[2][X_POS] - center_to_leg_center_distance
        leg_centers[3][Z_POS] = leg_centers[3][Z_POS] - center_to_leg_center_distance

        leg_length = self.map_size_half - self.intersection_len_half

        self.legs = []
        for i in range(4):
            self.legs.append( Leg(leg_centers[i], leg_length, i)  )

    def construct_lanes(self):
        for leg in self.legs:
            leg.lanes = ["" for i in range( self.num_of_lanes*2 )]
            lane_centers = np.tile(leg.leg_center, (self.num_of_lanes*2,1)) # self.num_of_lanes*2 is the num of total lanes on a leg
            
            if leg.direction_from_center % 2 == 0: # for x+ and x- legs
                lane_scale = np.array([leg.leg_length, 0, self.lane_width_half*2])
                for i in range(self.num_of_lanes): # for lanes in one direction
                    lane_center_to_leg_center = self.lane_width_half*(2*i + 1)
                    lane_centers[i][Z_POS] = lane_centers[i][Z_POS] + lane_center_to_leg_center
                    lane_centers[i+self.num_of_lanes][Z_POS] = lane_centers[i+self.num_of_lanes][Z_POS] - lane_center_to_leg_center

                    leg.lanes[i] = Lane(lane_centers[i], lane_scale, 2)
                    leg.lanes[i+self.num_of_lanes] = Lane(lane_centers[i+self.num_of_lanes], lane_scale, 0)
            else: # for z+ and z- legs
                lane_scale = np.array([self.lane_width_half*2, 0, leg.leg_length]) 
                for i in range(self.num_of_lanes):
                    lane_center_to_leg_center = self.lane_width_half*(2*i + 1)

                    lane_centers[i][X_POS] = lane_centers[i][X_POS] + lane_center_to_leg_center
                    lane_centers[i+self.num_of_lanes][X_POS] = lane_centers[i+self.num_of_lanes][X_POS] - lane_center_to_leg_center

                    leg.lanes[i] = Lane(lane_centers[i], lane_scale, 1)
                    leg.lanes[i+self.num_of_lanes] = Lane(lane_centers[i+self.num_of_lanes], lane_scale, 3)

def test_infrastructure(map_size_half=100, center=np.zeros(3), 
    intersection_len_half=10, lane_width_half=0.5, road_thickness=0.1, num_of_lanes=1):
    to_json = []
    c = Construct_legs(map_size_half=map_size_half, center=center, 
        intersection_len_half=intersection_len_half,
        lane_width_half=lane_width_half, road_thickness=road_thickness, 
        num_of_lanes=num_of_lanes)
    c.construct_legs()
    c.construct_lanes()
    for leg in c.legs:
        for lane in leg.lanes:
            print (lane)
            
            
            to_json.append(lane.__dict__)
    to_json.append(Intersection(center,intersection_len_half).__dict__)
    print ("_______________")
    print (to_json) 
    export_to_json(to_json, 'lanes_on_legs.json')



class Trajectory:
    def __init__(self):
        pass
    def get_travel_time(self, speed):
        pass
    def record_movement(self, interval):
        # cookies is a list of np.array, must be a list, for UNITY reading
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
    def __init__(self, np_positions):
        Trajectory.__init__(self)
        self.route = np_positions
    def get_travel_time(self, speed):
        time = self.route.shape[0]  /  speed
        return time
    def record_movement(self, speed):
        return self.route[::speed]



class Car:
    def __init__(self, position):
        self.position = position
    def set_trajectory(self):
        center = np.zeros(3)
        map_size_half=100
        intersection_len_half = 10
        self.trajectories = [
        Line_Trajectory(np.array([0.5,0,-map_size_half]), 
            np.array([0.5,0,-intersection_len_half])), 
        Circular_Trajectory(center, intersection_len_half, 
            -np.pi/2, np.pi/2),
        Line_Trajectory(np.array([0.5,0,intersection_len_half]), 
            np.array([0.5,0,map_size_half]))
        ]
        # this traj need some amendment because of the offset "0.5"!!
    def movement(self, speed):      
        # for the line trajectory
        self.positions = [ i.record_movement(speed)  for i in self.trajectories]
        self.positions = [ i for trajectory in self.positions for i in trajectory] # a list of nparray()
        self.positions = np.array(self.positions)
        #np.save("positions.np", self.positions)
        self.moves = [i-j \
            for i, j in zip(self.positions[:-1], self.positions[1:])]
         
    def export_movement(self, command='toWWW'):
        
        
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
            
            time.sleep(1) # "speed", by definition, is meter per second


def test_car_movement():
    map_size_half=100
    center=np.zeros(3)
    intersection_len_half=10
    lane_width_half=0.5
    road_thickness=0.1
    num_of_lanes=1
    c = Car(np.array([0.5,0,-map_size_half]))        
    c.set_trajectory()
    c.movement(0.5)
    c.export_movement('toWWW')



def launch_server():


    app = Flask(__name__)

    app.updated = False
    app.data_to_show = ''

    @app.route('/', methods=['POST', 'GET'])
    def index():
        if request.method == 'POST':
            app.updated = not app.updated
            # print("json:", request.data)
            app.data_to_show = request.data

        if app.updated:
            #app.updated = not app.updated
            
            return app.data_to_show
            return "app state 1\n"
        else:
            return app.data_to_show
            return "app state 2\n"
    #def update(): 
    #   @app.route('/')
    #   def index():
    #       return "Hello, World!"
    #updated = False
    app.run(debug=True)
    











if __name__ == "__main__":
    
    
    p0 = Process(target=launch_server)
    p0.start()
    time.sleep(3)
    print("----  start posting json  ----")
    p1 = Process(target=test_car_movement)
    p1.start()
    










            

