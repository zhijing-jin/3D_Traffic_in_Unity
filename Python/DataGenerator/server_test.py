from flask import Flask, request
import time
import threading
from global_assignments import *
from threading import Lock

page = ''

def sth():
    time.sleep(5)
    car_id = 1
    for i in range(100):
        export_to_www_json({'num': i}, url='http://127.0.0.1:5000/car00')
        # print(i)
        time.sleep(1)


def sthelse():
    time.sleep(5)
    car_id = 0
    for i in range(65, 122):
        export_to_www_json({'data': chr(i)}, url='http://127.0.0.1:5000/car01')
        # print(chr(i))
        time.sleep(1)




def launch_server():
    
    app = Flask(__name__)

    num = 10
    app.data = ''
    app.data_to_show = ['' for i in range(num)]

    @app.route('/', methods=['POST', 'GET'])
    def index():
        if request.method == 'POST':
            # print("json:", request.data)
            app.data = request.data

        return app.data

    car_id = 0

    @app.route('/car' + "%02d" % car_id, methods=['POST', 'GET'])
    def car00():
        insert_id = 0
        if request.method == 'POST':
            # print("json:", request.data)
            
            app.data_to_show[insert_id] = request.data
            

        return app.data_to_show[insert_id]

    car_id = 1

    @app.route('/car' + "%02d" % car_id, methods=['POST', 'GET'])
    def car01():
        
        insert_id = 1
        if request.method == 'POST':
            app.data_to_show[insert_id] = request.data
            

        return app.data_to_show[insert_id]

    app.run(debug=True, host='0.0.0.0')


def test():

    t = threading.Thread(target=sth)
    t.start()
    t2 = threading.Thread(target=sthelse)
    t2.start()
    launch_server()


if __name__ == '__main__':
    #updated = False
    test()

'''
{
    "movement": {
        "x": -0.009999999999999787,
        "y": 0.0,
        "z": 0.0
    },
    "position": {
        "x": -9.99,
        "y": 0.0,
        "z": 0.5
    }
}
'''
