from flask import Flask, request




def launch_server():
    
    app = Flask(__name__)

    num = 10
    app.data = ''
    app.data_to_show = ['' for i in range(num)]
    app.road_map = ''

    @app.route('/', methods=['POST', 'GET'])
    def index():
        if request.method == 'POST':
            # print("json:", request.data)
            app.data = request.data

        return app.data
    
    @app.route('/map', methods=['POST', 'GET'])
    def map():
        if request.method == 'POST':
            # print("json:", request.data)
            app.road_map = request.data

        return app.road_map

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



    car_id = 2
    @app.route('/car' + "%02d" % car_id, methods=['POST', 'GET'])
    def car02():
        
        insert_id = 2
        if request.method == 'POST':
            app.data_to_show[insert_id] = request.data
            

        return app.data_to_show[insert_id]



    car_id = 3
    @app.route('/car' + "%02d" % car_id, methods=['POST', 'GET'])
    def car03():
        
        insert_id = 3
        if request.method == 'POST':
            app.data_to_show[insert_id] = request.data
            
        return app.data_to_show[insert_id]


    app.run(debug=True, host='0.0.0.0')



if __name__ == '__main__':
    #updated = False
    launch_server()
    