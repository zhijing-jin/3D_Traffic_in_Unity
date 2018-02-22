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
    
