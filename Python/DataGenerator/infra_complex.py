from global_assignments import *
# from .global_assignments import *
import math
from collections import defaultdict
import threading


coordinate_prec = 2
chann_ls = []
world = None
cars = []
car_ls = []
reso=0.01


class mydefaultdict(defaultdict):
    def __missing__(self, key):
        self[key] = new = self.default_factory(key)
        return new
class Chann_Seg:
    def __init__(self, chann_id, position, next_pos, prev_pos, scale, 
        rotation, carid=None, maxspeed=5):        
        self.chann_id = chann_id
        self.carid = carid
        self.maxspeed = maxspeed        

        position = np.around(position, decimals=coordinate_prec)
        prev_pos = np.around(prev_pos, decimals=coordinate_prec)
        next_pos = np.around(next_pos, decimals=coordinate_prec)
        # transform np.array of (3,) into Vector3 for Unity 
        self.position = {"x": position[X_POS],
                        "y": position[Y_POS],
                        "z": position[Z_POS]}
        self.next_pos = {"x": next_pos[X_POS],
                        "y": next_pos[Y_POS],
                        "z": next_pos[Z_POS]}
        self.prev_pos = {"x": prev_pos[X_POS],
                            "y": prev_pos[Y_POS],
                            "z": prev_pos[Z_POS]}
        self.scale = {"x": scale[X_POS],
                      "y": scale[Y_POS],
                      "z": scale[Z_POS]}
        self.rotation={"x": rotation[X_POS],
                      "y": rotation[Y_POS],
                      "z": rotation[Z_POS]}
    def __repr__(self): # for printing out the class as a string
        return str(self.__dict__)
class Point:
    def __init__(self, chann_id, chann_order, carid):
        self.chann_ls = chann_id #= []
        # self.chann_order = chann_order#= []
        self.carid = carid # []
    def __repr__(self): # for printing out the class as a string
        return str(self.__dict__)    

              
class Construct_Chann:
    def __init__(self, lane_width_half=0.5, road_thickness=0.01,
        map_size_half=100, center=np.zeros(3)):
        self.map_size_half = map_size_half
        self.center = center
        self.scale = [ lane_width_half*2,
                     road_thickness,
                     None]
        self.reso = reso
        self.lane_width_half = lane_width_half
    def construct_chann(self):
        global chann_ls

        w = self.lane_width_half
        reso = self.reso
        xs, zs = [], []
        chann_ls = [{}, {}]

        
        x = np.linspace(w, w, num=10//reso)
        z = np.linspace(-10, 0, num=10//reso) # (lane_width_half, this_pos)
        xs.extend(list(x))
        zs.extend(list(z))

        x = np.linspace(w, 0, num=w//reso)
        z = np.linspace(0, w, num=w//reso)
        xs.extend(list(x))
        zs.extend(list(z))


        x = np.linspace(0, -10, num=10//reso)
        z = np.linspace(w, w, num=10//reso)
        xs.extend(list(x))
        zs.extend(list(z))

        ys = [0 for x in xs]
        prev_pos = zip(xs, ys, zs)
        prev_pos = np.array([(i, j, k) for i, j, k in prev_pos])




        r = 10  
        d_angle = reso / r # len_curve / radius = angle  
        seg_num = math.ceil(2 * np.pi * r / reso)
        prev_pos = [ r * 
                (self.center + np.array([np.cos(i*d_angle), 0, np.sin(i*d_angle)]))
                        for i in range(seg_num)]

        
        
        # pos = np.around(pos, decimals=coordinate_prec)
        pos = prev_pos[1:]
        next_pos = pos[1:]
        for p_p, p, n_p in zip(prev_pos, pos, next_pos):
            delta = n_p - p
            self.scale[Z_POS] = np.linalg.norm(delta)
            rot = - np.arctan(delta[Z_POS]/delta[X_POS]) / np.pi * 180 + 90
            rot = np.array([0, rot, 0])

            p = np.around(p, decimals=coordinate_prec)
            
            chann_ls[0][(p[0], p[2])] = (Chann_Seg(0, p, n_p, p_p,
                self.scale, rot))

        # # a straight line    
        # x = np.linspace(-10, 10, 20/reso)
        # x = x.reshape([-1, 1])
        # y = x * 0
        # z = y - w
        # prev_pos = np.hstack((x, y, z))

        # pos = prev_pos[1:]
        # next_pos = pos[1:]
        
        

        # for p_p, p, n_p in zip(prev_pos, pos, next_pos):
        #     delta = n_p - p
        #     self.scale[Z_POS] = np.linalg.norm(delta)
        #     rot = - np.arctan(delta[Z_POS]/delta[X_POS]) / np.pi * 180 + 90
        #     rot = np.array([0, rot, 0])

        #     p = np.around(p, decimals=coordinate_prec)


        #     chann_ls[1][(p[0], p[2])] = (Chann_Seg(1, p, n_p, p_p,
        #         self.scale, rot))
        print(chann_ls)
class World:
    def __init__(self, chann_ls, map_size_half=100, prec=coordinate_prec):
        self.chann_ls = chann_ls
        self.map_size_half = map_size_half
        self.prec = prec # num of decimal points of a loc in world
    def construct_world(self):
        global world
        size = self.map_size_half
        world = defaultdict(lambda: Point([],[],None))        
        for chann in self.chann_ls:
            for seg in chann:
                seg = chann[seg]
                key = (seg.position['x'], seg.position['z'])
                world[key].chann_ls.append(seg.chann_id)
                if seg.carid:
                    assert world[key].carid == None
                    world[key].carid = carid
        # update chann_ls as priority list
        world = {key: world[key] for key in world}
        print (world)




class Car:
    def __init__(self, chann_id, pos, speed ):
        global world, car_ls
        self.chann_id = chann_id
        self.position = {"x": pos[X_POS],
                        "y": pos[Y_POS],
                        "z": pos[Z_POS]}
        self.next_pos = chann_ls[chann_id][(pos[X_POS], pos[Z_POS])].next_pos
        
        self.speed = speed # progress per frame 
        self.active = True
        self.positions = []
        self.facing = []
        world[(pos[X_POS], pos[Z_POS])].carid = len(car_ls)
        car_ls.append(self)
        self.car_id = world[(pos[X_POS], pos[Z_POS])].carid
    def change_chann(self, to_chann, lane_width_half, eps=0.01):
        w = lane_width_half
        pos = np.array((self.position['x'], self.position['z']))
        next_pos = np.array((self.next_pos['x'], self.next_pos['z']))
        delta = next_pos - position

        if lane_change:
            candi_chann = []
            #check changeable lanes
            shift = np.array(delta[1], -delta[0])
            shift = shift / np.linalg.norm(shift) * w * 2
            neigh = pos + shift

            range_x_s = neigh[0] - delta[0]/2
            range_x_e = neigh[0] + delta[0]/2
            range_y_s = neigh[1] - delta[1]/2
            range_y_e = neigh[1] + delta[1]/2
            range_x = np.linspace(range_x_s, range_x_e, num=(range_x_s - range_x_e)//coordinate_prec)
            range_y = np.linspace(range_y_s, range_y_e, num=(range_y_s - range_y_e)//coordinate_prec)
            range_x = np.around(range_x, decimals=coordinate_prec)
            range_y = np.around(range_y, decimals=coordinate_prec)
            for x, y in zip(range_x, range_y):
                if world[(x,y)].chann_ls:
                    for chann_id in world[(x,y)].chann_ls:
                        if chann_ls[chann_id][(x,y)].rotation - \
                            self.rotation < eps:
                            candi_chann.append((chann_id, (x,y)))
            for chann_id, (x,y) in candi_chann:
                pass
        elif turn:
            candi_chann = []

            ls = world[tuple(pos)].chann_ls - [self.chann_id]
            for chann_id in ls:
                n_p = chann_ls[chann_id][tuple(pos)].next_pos
                n_p = np.array((n_p['x'], n_p['z']))
                if (n_p - next_pos)[1] >= 0:
                    candi_chann.append((chann_id, tuple(pos)))
            for chann_id, (x,y) in candi_chann:
                pass        
    def speedup(self):
        pos = self.position
        pos = (pos['x'], pos['z'])
        self.speed = chann_ls[self.chann_id][pos].maxspeed

        # if there is a car in the same lane
        for __ in np.linspace(0, self.speed, num=self.speed // reso):
            if pos in chann_ls[self.chann_id]:
                pos = chann_ls[self.chann_id][pos].next_pos
                pos = (pos['x'], pos['z'])

                if pos in world:
                    
                    if world[pos].carid != None:
                        print("a car in the front", pos, world[pos])
                        if car_ls[world[pos].carid].speed < self.speed:
                            self.speed = car_ls[world[pos].carid].speed + __ 
                            print("speed changed:", self.speed)
                            break
                
            else:
                print("same line but end")
                self.active = False
                break

        # if there is a shared vertex
        pos = self.position
        pos = (pos['x'], pos['z'])

        for __ in np.linspace(0, self.speed, num=self.speed // reso):
            pos = chann_ls[self.chann_id][pos].next_pos
            pos = (pos['x'], pos['z'])

            if pos in world:
                prior = world[pos].chann_ls.index(self.chann_id)
                for chann_id in world[pos].chann_ls[:prior]:
                    danger_range = chann_ls[chann_id][pos].maxspeed #nearby car speed
                    p = pos
                    for dista in np.linspace(0, danger_range, num=danger_range// reso):
                        p = chann_ls[chann_id][p].prev_pos
                        p = (p['x'], p['z'])
                        if world[pos].carid != None:
                            if cars[world[pos].carid].speed == dista:
                                self.speed = __ - reso

                                break
            else:
                print("shared vertex")
                self.active = False
                break

    def go(self):
        pos = self.position
        pos = (pos['x'], pos['z'])
        pos_per_frame = [pos]
        fac_per_frame = []

        for __ in np.linspace(0, self.speed, num=self.speed// reso):
            if pos in chann_ls[self.chann_id]:
                self.position = chann_ls[self.chann_id][pos].next_pos
                pos = (self.position['x'], self.position['z'])
                pos_per_frame.append(pos)
                fac_per_frame.append((pos_per_frame[-1][0] - pos_per_frame[-2][0], pos_per_frame[-1][1] - pos_per_frame[-2][1]))
            else:
                self.active = False
                break
        self.positions.append(pos_per_frame)  
        self.facing.append(fac_per_frame)      
    def move(self, speedup=False):
        if self.active:
            if speedup:
                self.speedup()
            self.go()
    def export_movement(self, framerate=1000):   
        data = {}
        self.positions = [[np.array([pos[X_POS], 0, pos[1]]) for pos in pos_per_frame] for pos_per_frame in self.positions]
        self.facing = [[np.array([fac[X_POS], 0, fac[1]]) for fac in fac_per_frame] for fac_per_frame in self.facing]
        
        with open("Trace.txt", 'w') as fwrite:
            for m in self.facing:
                for i in m:
                    fwrite.write(' '.join([str(j) for j in list(i)]) + '\n')
                fwrite.write('\n\n')
        with open("Moves.txt", 'w') as fwrite:
            for m in self.positions:
                for i in m:
                    fwrite.write(' '.join([str(j) for j in list(i)]) + '\n')
                fwrite.write('\n\n')
        
        url = 'http://127.0.0.1:5000/car' + "%02d" % self.car_id
        for frame in range(len(self.positions)):
            fac_per_frame = self.facing[frame]
            pos_per_frame = self.positions[frame]
            for move, pos in zip(fac_per_frame, pos_per_frame[:-1]):
                data["movement"] = nparray_to_vector3(move)
                data["position"] = nparray_to_vector3(pos)
                            
                # filename = "/home/zhi/Downloads/6100/unity/FancyIntersection/Assets/Resources/DataForSettings/VehicleData/cars_realtime_updates.json"
                # export_to_json(data, filename)
                export_to_www_json(data, url='http://127.0.0.1:5000/car' + "%02d" % self.car_id)    
                time.sleep(1.0/framerate / len(fac_per_frame)) # "speed", by definition, is meter per second





                    





        
            
        


def draw_cir(tofile='../data/lane_positions.json', map_size_half=100, center=np.zeros(3), intersection_len_half=10,
        lane_width_half=0.5, road_thickness=0.01, seg_len=1):
    line_list = []
    c = Construct_Chann()
    c.construct_chann()
    
    w = World(chann_ls)
    w.construct_world()

    

    for chann in chann_ls:
        for seg in chann:
            line_list.append(chann[seg].__dict__)
    #print ("_______________")
    #print (to_json) 
    to_json = {"LineList": line_list}
    export_to_json(to_json, tofile)
    export_to_www_json(to_json, url='http://127.0.0.1:5000/map')

    print ("_______________")
    print ("_______________")
    spawn_cars()
    
    

def spawn_cars():
    cars = [None for i in range(1)]
    cars[0] = Car(0, (-8.39, 0, -5.44), 2)

    car_running = True
    while car_running:
        car_running = False
        for i in range(1):
            if cars[i].active:
                cars[i].move()
                print(cars[i].speed)

                car_running = True
                
    
    t = [None for __ in range(1)]
    

    for i in range(1):
        t[i] = threading.Thread(target=cars[i].export_movement)
        t[i].start()
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
    

    draw_cir()

if __name__ == "__main__":
	test_infrastructure()