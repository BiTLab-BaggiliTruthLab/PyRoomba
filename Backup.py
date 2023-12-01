import pprint
import requests,urllib.parse,getpass,logging,argparse
from AwsRequest import AwsRequest
from flask import Flask, request, jsonify, render_template, session,send_file, render_template_string
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import io
import json
import matplotlib.patches as patches
import numpy as np 
import getpass
import datetime
from io import BytesIO
import matplotlib.lines as mlines
import uuid

class IrobotAuthorization:
    app_id = None
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        response = requests.get("https://disc-prod.iot.irobotapi.com/v1/discover/endpoints?country_code=US")
        res_json = response.json()
        deployment = res_json['deployments'][next(iter(res_json['deployments']))]
        self.httpBase = deployment['httpBase']
        iotBase = deployment['httpBaseAuth']
        iotUrl = urllib.parse.urlparse(iotBase)
        self.iotHost = iotUrl.netloc
        region = deployment['awsRegion']
        self.apikey = res_json['gigya']['api_key']
        #print('self.apikey',self.apikey)
        self.gigyaBase = res_json['gigya']['datacenter_domain']
        data = {"apiKey": self.apikey,
                "targetenv": "mobile",
                "loginID": self.username,
                "password": self.password,
                "format": "json",
                "targetEnv": "mobile",
                }
        response = requests.post(
            "https://accounts.%s/accounts.login" % self.gigyaBase, data=data)
        res_json = response.json()
        #print(f"account_login_json: {res_json}")
        uid = res_json['UID']
        uidSig = res_json['UIDSignature']
        sigTime = res_json['signatureTimestamp']
        profile = res_json['profile']
        global app_id
        # data = {
        #     "id": uuid.uuid4()
        # }
        # # Convert the UUID to a string
        # data["id"] = str(data["id"])

        # # Serialize to JSON
        # app_id = json.dumps(data)
        # print(app_id)

        app_id = "ANDROID-" + str(uuid.uuid4()).upper()
        print(app_id)
        data = {
            "app_id": app_id,#"ANDROID-67815113-1C34-473E-B8F2-77BF1A444395",
            "assume_robot_ownership": "0",
            "gigya": {
                "signature": uidSig,
                "timestamp": sigTime,
                "uid": uid,
            }
        }
        response = requests.post("%s/v2/login" % self.httpBase, json=data)
        res_json = response.json()
        #print(f"v2_login_json: {res_json}")
        access_key = res_json['credentials']['AccessKeyId']
        secret_key = res_json['credentials']['SecretKey']
        session_token = res_json['credentials']['SessionToken']
        self.data = res_json
        self.amz = AwsRequest(region, access_key, secret_key,
                              session_token, "execute-api")
        
        
    def get_details(self):
        return self.data['robots']
    
    def get_credentials(self):
        robot_keys = self.data['robots'].keys()
        device_id = next(iter(robot_keys))
        return device_id
    
    def info(self):
        return self.data


    def get_maps(self, robot):
        r = (self.amz.get(self.iotHost, '/v1/%s/pmaps' % robot, query="activeDetails=2")).json()
        pmaps = []
        for map_dict in r:
            pmap_id = map_dict['pmap_id']
            pmapv_id = map_dict['active_pmapv_details']['active_pmapv']['pmapv_id']
            pmaps.append([pmap_id, pmapv_id])
            return pmaps
    
    def view_maps(self,robot,pmap,pmapv):
        r = (self.amz.get(self.iotHost, '/v1/%s/pmaps/%s/versions/%s/umf' % (robot,pmap,pmapv), query="activeDetails=2")).json()
        return r
     
    def view_mission_history(self, robot):
       #r = (self.amz.get(self.iotHost, '/v1/%s/missionhistory' % robot, query="filterType=omit_quickly_canceled_not_scheduled&supportedDoneCodes=dndEnd,returnHomeEnd&app_id=ANDROID-67815113-1C34-473E-B8F2-77BF1A444395")).json()
       r = (self.amz.get(self.iotHost, '/v1/robots/%s' % (robot), query="app_id=%s" % app_id)).json()
       print("getmapJson==>",r)
       return r

     
         

def plot_map(points2d, borders, poses2d,typed_poses):
    # Create figure and axes
     fig, ax = plt.subplots()
        # Prepare to plot borders
     for border in borders:
            border_coordinates = [points2d[id] for id in border['geometry']['ids'][0]]
            border_polygon = patches.Polygon(border_coordinates, fill=True, alpha=0.3)
            ax.add_patch(border_polygon)
        # Prepare to plot poses
     for pose in poses2d:
            x, y = pose['coordinates']
            ori_rad = pose['ori_rad']
            dx, dy = np.cos(ori_rad), np.sin(ori_rad)
            ax.arrow(x, y, dx, dy, head_width=0.05, head_length=0.1, fc='black', ec='black')
        # Prepare to plot typed poses
     start_pose_ids = typed_poses['start_pose']['geometry']['ids']
     end_pose_ids = typed_poses['end_pose']['geometry']['ids']
     dock_pose_ids = typed_poses['dock_poses']['geometry']['ids']

     if start_pose_ids:
      x, y = points2d[start_pose_ids[0]]
      start_dot = ax.plot(x, y, 'go', label='Start point')[0]  # start poses in green
     for id in start_pose_ids:
            x, y = points2d[id]
            ax.plot(x, y, 'go')  # start poses in green
      # Add the first end point to the plot with a label
     if end_pose_ids:
        x, y = points2d[end_pose_ids[0]]
        end_dot = ax.plot(x, y, 'ro', label='End point')[0] 
     for id in end_pose_ids:
                x, y = points2d[id]
                ax.plot(x, y, 'ro')  # end poses in red
     for id in dock_pose_ids:
                x, y = points2d[id]
                ax.plot(x, y, 'bo')  # dock poses in blue
     arrow_legend = mlines.Line2D([], [], color='black', marker='>', linestyle='-', label='robot direction')
    # This line will add the legend
     #plt.legend(handles=[start_dot, end_dot, arrow_legend], loc='upper left', bbox_to_anchor=(1, 1))
     plt.legend(handles=[arrow_legend, start_dot, end_dot], bbox_to_anchor=(1, 1), loc='upper right', fontsize='x-small')
     ax.set_aspect('equal', adjustable='datalim')
     buf = io.BytesIO()
     canvas = FigureCanvas(fig)
     canvas.print_png(buf)
     plt.close(fig)  # Close the figure to free up memory
     buf.seek(0)
     return buf


app = Flask(__name__)
app.secret_key = 'this-is-a-secret-key'


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    session['username'] = username
    session['password'] = password
    irobot_auth = IrobotAuthorization(username, password)
    irobot_auth.login()
    robotDetails = irobot_auth.get_details()
    robot_id = list(robotDetails.keys())[0]
    robot_info = robotDetails[robot_id]
    robot_password = robot_info['password'] 
    sku = robot_info['sku']
    user_cert = robot_info['user_cert']
    soft_version = robot_info['softwareVer']
    robot_name = robot_info['name']
    # Store the irobot_auth instance in the session or a global variable, so that it can be accessed later in other routes
    session['logged_in'] = True
    return jsonify({"status": "success"})

@app.route('/map_json', methods=['GET'])
def map_json():
    with open('map.json', 'r') as f:
        map_data = json.load(f)
    return jsonify(map_data)

@app.route('/maps', methods=['GET'])
def g_maps():

 # Check if the user is logged in
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"})
   # Retrieve the username and password from the session
    username = session.get('username')
    password = session.get('password')
    irobot_auth = IrobotAuthorization(username, password)
    irobot_auth.login()
    robotID = irobot_auth.get_credentials()
    #print("robotId==>",robotID)
    pmaps = irobot_auth.get_maps(robotID)
    return jsonify({"robotID": robotID, "pmaps": pmaps})



@app.route('/all_maps', methods=['GET'])
def all_maps():

    # Check if the user is logged in
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"})
    # Retrieve the username and password from the session
    username = session.get('username')
    password = session.get('password')
    # Create a new irobot_auth instance
    irobot_auth = IrobotAuthorization(username, password)
    irobot_auth.login()
    # Get the robot ID
    robotID = irobot_auth.get_credentials()
    # Get the maps related to this robot
    robot_maps = irobot_auth.get_maps(robotID)
    # Prepare a result list
    result = []
    # If there's only one map, print it
    if len(robot_maps) == 1:
        result.append({"robot_id": robotID, "map": robot_maps[0]})
    else:
        # Enumerate all maps
        for i, map in enumerate(robot_maps):
            result.append({"robot_id": robotID, "map_number": i+1, "map": map})
    return jsonify(result)



@app.route('/view_map/<robotID>/<pmapID>/<pmapv>', methods=['GET'])
def view_map(robotID, pmapID,pmapv):
    # Retrieve the irobot_auth instance from the session or global variable
    # Check if the user is logged in
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"})
    # Retrieve the username and password from the session
    username = session.get('username')
    password = session.get('password')
    # Create a new irobot_auth instance
    irobot_auth = IrobotAuthorization(username, password)
    irobot_auth.login()
    # Get the map data
    map_data = irobot_auth.view_maps(robotID, pmapID,pmapv)
    maps= map_data['maps']
    map_name = map_data['maps'][0]['map_header']['name']
    points2d = {}
    for point in map_data['maps'][0]['points2d']:
      id_ = int(point['id'])
      coordinates = point['coordinates']
      points2d[id_] = coordinates
    borders = []
    for border in map_data['maps'][0]['borders']:
     ids = [[int(id_) for id_ in region] for region in border['geometry']['ids']]
     new_border = {
        "free_type": border["free_type"],
        "geometry": {
            "ids": ids,
            "type": border["geometry"]["type"] 
        },
        "id": border["id"]
    }
    borders.append(new_border)
    poses2d = []
    for pose in map_data['maps'][0]['poses2d']:
        new_pose = {
            "coordinates": pose["coordinates"],
            "id": int(pose["id"]), 
            "ori_rad": pose["ori_rad"]
        }
        poses2d.append(new_pose)
    typed_poses = {}
    for pose_type, pose in map_data['maps'][0]['typed_poses'].items():
        new_pose = {
            "geometry": {
                "ids": [int(id_) for id_ in pose["geometry"]["ids"]],
                "type": pose["geometry"]["type"]
            }
        } 
        typed_poses[pose_type] = new_pose
    #print("typed_poses",typed_poses)
    img = plot_map(points2d, borders, poses2d,typed_poses)
    #return render_template_string("<script>console.log('{{message}}');</script>", message=map_data)
    return send_file(img, mimetype='image/png')
  

# @app.route('/map_view', methods=['GET'])
# def map_view():
#     return render_template('map_view.html') 

@app.route('/view_map_brief/<robotID>/<pmapID>/<pmapv>', methods=['GET'])
def view_map_brief(robotID, pmapID,pmapv):
    # Check if the user is logged in
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"})

    # Retrieve the username and password from the session
    username = session.get('username')
    password = session.get('password')

    # Create a new irobot_auth instance
    irobot_auth = IrobotAuthorization(username, password)
    irobot_auth.login()

    # Get the map data
    map_data = irobot_auth.view_maps(robotID, pmapID,pmapv)
    print(json.dumps(map_data, indent=4))
    id = map_data['maps'][0]['map_header']['id']
    version = map_data['maps'][0]['map_header']['version']
    map_name = map_data['maps'][0]['map_header']['name']
    create_time = map_data['maps'][0]['map_header']['create_time']
    create_time = datetime.datetime.fromtimestamp(create_time)
    learning_percentage = map_data['maps'][0]['map_header']['learning_percentage']
    resolution = map_data['maps'][0]['map_header']['resolution']
    user_orientation_rad = map_data['maps'][0]['map_header']['user_orientation_rad']
    robot_orientation_rad = map_data['maps'][0]['map_header']['robot_orientation_rad']
    area = map_data['maps'][0]['map_header']['area']
    version = map_data['maps'][0]['map_header']['version']
    nmssn = map_data['maps'][0]['map_header']['nmssn']
    mission_id = map_data['maps'][0]['map_header']['mission_id']

   
    return jsonify({"id":id,"version":version,"map_name": map_name, "create_time": create_time,"learning_percentage":learning_percentage
                    ,"resolution": resolution,"user_orientation_rad":user_orientation_rad,"robot_orientation_rad":robot_orientation_rad,
                    "area":area,"version":version,"nmssn":nmssn,"mission_id":mission_id})

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/info', methods=['GET'])
def info():

     if not session.get('logged_in'):
      return jsonify({"error": "Not logged in"})

# Retrieve the username and password from the session
     username = session.get('username')
     password = session.get('password')

    # Create a new irobot_auth instance
     irobot_auth = IrobotAuthorization(username, password)
     irobot_auth.login()

     robotDetails = irobot_auth.get_details()
     robot_id = list(robotDetails.keys())[0]
     robot_info = robotDetails[robot_id]
     robot_password = robot_info['password'] 
     sku = robot_info['sku']
     user_cert = robot_info['user_cert']
     soft_version = robot_info['softwareVer']
     robot_name = robot_info['name']
     return jsonify({"robot_id": robot_id,"robot_password":robot_password,"sku":sku,"user_cert":user_cert,"soft_version":soft_version,"robot_name":robot_name})

@app.route('/mission_history', methods=['GET'])
def mission_history():
    if not session.get('logged_in'):
      return jsonify({"error": "Not logged in"})

# Retrieve the username and password from the session
    username = session.get('username')
    password = session.get('password')

    # Create a new irobot_auth instance
    irobot_auth = IrobotAuthorization(username, password)
    irobot_auth.login()

    robotDetails = irobot_auth.get_details()
    robot_id = list(robotDetails.keys())[0]
    mission_history = irobot_auth.view_mission_history(robot_id)
    return mission_history
    #return jsonify(mission_history), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)