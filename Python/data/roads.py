This is the overall guideline od road construction

(0) GLOBAL PARAMS
MAP_SIZE_half,	CENTER,	INTERSETCION_half_len,		
800;0,0,0;100;
lane_width_half:0.5,
road_thickness:0.1
num_of_lanes:1

(1) LEG CONSTRUCTION
And then the affected roads are:

4 legs:
leg_center = center + (INTERSETCION_half_len + MAP_SIZE_half)/2
leg_length = MAP_SIZE_half - INTERSETCION_half_len
0,1,2,3 -> x+, z+, x-, z-

(2) LANE CONSTRUCTION
And in each leg: 
lane1: lane_center = leg_center + (0,0, lane_width_half*(2*num_of_lanes -1) )
lane_scale = (lane_width_half*2, leg_length)

lane_direction:
leg 0x+; (ct z+, dir2), (ct z-, dir0); scale(len, 0, width);
leg 1z+; (ct x+, dir1), (ct x-, dir3) ;
leg 2x-; (ct z+, dir2), (ct z-, dir0) ; scale(len, 0, width);
leg 3z-; (ct x+, dir1), (ct x-, dir3);

EXAMPLE:
{'lane_center': array([ 450. ,    0. ,    0.5]), 'scale': array([ 700.,    0.,    1.]), 'traffic_direction': 2}
{'lane_center': array([ 450. ,    0. ,   -0.5]), 'scale': array([ 700.,    0.,    1.]), 'traffic_direction': 0}
{'lane_center': array([   0.5,    0. ,  450. ]), 'scale': array([   1.,    0.,  700.]), 'traffic_direction': 1}
{'lane_center': array([  -0.5,    0. ,  450. ]), 'scale': array([   1.,    0.,  700.]), 'traffic_direction': 3}
{'lane_center': array([-450. ,    0. ,    0.5]), 'scale': array([ 700.,    0.,    1.]), 'traffic_direction': 2}
{'lane_center': array([-450. ,    0. ,   -0.5]), 'scale': array([ 700.,    0.,    1.]), 'traffic_direction': 0}
{'lane_center': array([   0.5,    0. , -450. ]), 'scale': array([   1.,    0.,  700.]), 'traffic_direction': 1}
{'lane_center': array([  -0.5,    0. , -450. ]), 'scale': array([   1.,    0.,  700.]), 'traffic_direction': 3}

{
	"somewords":"hi you succeed!",
	"speed":"1",
	"scale":{
            "x": -0.47753495,
            "y": -0.184191,
            "z": -0.8590891             
           },
    "position":{
    		"x": 10,
    		"y": 10,
    		"z": 10	
    		}

}