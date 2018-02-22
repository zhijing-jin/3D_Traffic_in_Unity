from .global_assignments import *
import math

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
class Lane_Seg(Lane):
    def __init__(self, position, scale, traffic_direction, rotation):
        super(Lane_Seg,self).__init__(position, scale, traffic_direction)
        self.rotation={"x": rotation[X_POS],
                      "y": rotation[Y_POS],
                      "z": rotation[Z_POS]}

class Intersection:
    def __init__(self, center, intersection_len_half, road_thickness):
        self.position = {"x": center[X_POS],
                        "y": center[Y_POS],
                        "z": center[Z_POS]}
        self.scale = {"x": 2*intersection_len_half,
                    "y": road_thickness,
                    "z": 2*intersection_len_half}
                        
class Construct_Circle:
    def __init__(self, map_size_half=100, center=np.zeros(3), intersection_len_half=10,
        lane_width_half=0.5, road_thickness=0.01, seg_len=1):
        self.map_size_half = map_size_half
        self.center = center
        self.scale = [ lane_width_half*2,
                     road_thickness,
                     seg_len]
        self.seg_len = seg_len
    def construct_cir(self):
        r = self.map_size_half  
        d_angle = self.seg_len / r # len_curve / radius = angle  
        seg_num = math.ceil(2 * np.pi * r / self.seg_len)
        pos = [ r * 
                (self.center + np.array([np.cos(i*d_angle), 0, np.sin(i*d_angle)]))
                        for i in range(seg_num)]
        rot = [np.array([0, -(i*d_angle) * 180 / np.pi, 0])
                        for i in range(seg_num)]
        print(rot)
        self.lanes = [Lane_Seg(p, self.scale, None, r) 
            for p, r in zip(pos, rot)]
        



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
                lane_scale = np.array([leg.leg_length, self.road_thickness, self.lane_width_half*2])
                for i in range(self.num_of_lanes): # for lanes in one direction
                    lane_center_to_leg_center = self.lane_width_half*(2*i + 1)
                    lane_centers[i][Z_POS] = lane_centers[i][Z_POS] + lane_center_to_leg_center
                    lane_centers[i+self.num_of_lanes][Z_POS] = lane_centers[i+self.num_of_lanes][Z_POS] - lane_center_to_leg_center

                    leg.lanes[i] = Lane(lane_centers[i], lane_scale, 2)
                    leg.lanes[i+self.num_of_lanes] = Lane(lane_centers[i+self.num_of_lanes], lane_scale, 0)
            else: # for z+ and z- legs
                lane_scale = np.array([self.lane_width_half*2, self.road_thickness, leg.leg_length]) 
                for i in range(self.num_of_lanes):
                    lane_center_to_leg_center = self.lane_width_half*(2*i + 1)

                    lane_centers[i][X_POS] = lane_centers[i][X_POS] + lane_center_to_leg_center
                    lane_centers[i+self.num_of_lanes][X_POS] = lane_centers[i+self.num_of_lanes][X_POS] - lane_center_to_leg_center

                    leg.lanes[i] = Lane(lane_centers[i], lane_scale, 1)
                    leg.lanes[i+self.num_of_lanes] = Lane(lane_centers[i+self.num_of_lanes], lane_scale, 3)
def draw_cir(tofile='../data/lane_positions.json', map_size_half=100, center=np.zeros(3), intersection_len_half=10,
        lane_width_half=0.5, road_thickness=0.01, seg_len=1):
    line_list = []
    c = Construct_Circle(map_size_half=map_size_half, center=center, intersection_len_half=intersection_len_half,
        lane_width_half=lane_width_half, road_thickness=road_thickness, seg_len=seg_len)
    c.construct_cir()
    
    for lane in c.lanes:
        line_list.append(lane.__dict__)
    #print ("_______________")
    #print (to_json) 
    to_json = {"LineList": line_list}
    export_to_json(to_json, tofile)
def draw_intersection(tofile='../data/lane_positions.json', map_size_half=100, center=np.zeros(3), intersection_len_half=10,
        lane_width_half=0.5, road_thickness=0.01, num_of_lanes=1):
    line_list = []
    c = Construct_legs(map_size_half=map_size_half, center=center, intersection_len_half=intersection_len_half,
        lane_width_half=lane_width_half, road_thickness=road_thickness, num_of_lanes=num_of_lanes)
    c.construct_legs()
    c.construct_lanes()
    for leg in c.legs:
        for lane in leg.lanes:
            # print (lane)
            
            
            line_list.append(lane.__dict__)
    line_list.append(Intersection(center,intersection_len_half,road_thickness).__dict__)
    #print ("_______________")
    #print (to_json) 
    to_json = {"LineList": line_list}
    export_to_json(to_json, tofile)
def test_infrastructure(tofile='../data/lane_positions.json', 
    map_size_half=100, center=np.zeros(3), intersection_len_half=10,
        lane_width_half=0.5, road_thickness=0.01, num_of_lanes=1, seg_len=1):
    draw_cir(tofile=tofile, map_size_half=map_size_half, center=center,
        intersection_len_half=intersection_len_half, lane_width_half=lane_width_half,
        road_thickness=road_thickness, seg_len=seg_len)

if __name__ == "__main__":
	test_infrastructure()