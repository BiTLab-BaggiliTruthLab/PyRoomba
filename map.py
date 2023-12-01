# import json
# import matplotlib.pyplot as plt

# # Load the JSON data
# with open('map.json') as f:
#     data = json.load(f)

# border_nums = data['umf']['maps'][0]['borders'][0]['geometry']['ids']
# border_layer = data['umf']['maps'][0]['points2d']

# # Create a dictionary mapping border IDs to coordinates
# id_to_coord = {}
# for point in border_layer:
#     id_to_coord[point['id']] = point['coordinates']

# # Get the coordinates associated with border_nums IDs
# border_coords = [id_to_coord[id] for id in border_nums[0]]




# # Loop through all layers in the map
# for layer in data['umf']['maps'][0]['layers']:
    
#     # Check the layer type and get the corresponding coordinates
#     if layer['layer_type'] == 'coverage':
#         coverage_layer = layer['geometry']['coordinates']

#     elif layer['layer_type'] == 'coverage_poly':
#         coverage_poly_layer = layer['geometry']['coordinates']
#         coverage_poly_layer = coverage_poly_layer[0][0] # Get the first set of coordinates


#         print('Coverage poly layer coordinates:', coverage_poly_layer)

# print("cov layer\n\n",coverage_layer)
# print ("cov_poly\n\n",coverage_poly_layer)
# print("border \n\n",border_nums)
# print("border \n\n",border_coords)


# # Create a figure and axes
# fig, ax = plt.subplots()

# # Plot the border coordinates
# x, y = zip(*border_coords)
# ax.plot(x, y,label='Border')

# # Plot the coverage layer coordinates
# x, y = zip(*coverage_poly_layer)
# ax.scatter(x, y, label='Coverage')



# # Show the plot
# plt.show()

# import json
# import matplotlib.pyplot as plt
# import numpy as np

# # Load JSON data
# with open('mapData.json') as f:
#   data = json.load(f) 

# # Extract coordinates
# outer_points = [(p['coordinates'][0], p['coordinates'][1]) for p in data['maps'][0]['points2d'] if p['id'].startswith('10000')]
# rug_points = [(p['coordinates'][0], p['coordinates'][1]) for p in data['maps'][0]['points2d'] if p['id'].startswith('1000')]
# start_pose = data['maps'][0]['poses2d'][0]

# # Create plot
# fig, ax = plt.subplots()

# # Draw outer boundary 
# for i in range(len(outer_points)-1):
#   ax.plot([outer_points[i][0], outer_points[i+1][0]],
#           [outer_points[i][1], outer_points[i+1][1]], 'black')
          
# # Fill floor
# ax.fill([p[0] for p in outer_points], 
#        [p[1] for p in outer_points],
#        'tan')
       
# #Draw rug  
# for i in range(len(rug_points)-1):
#   ax.plot([rug_points[i][0], rug_points[i+1][0]], 
#          [rug_points[i][1], rug_points[i+1][1]], 'darkgreen')
         
# # Draw start pose
# ax.plot(start_pose['coordinates'][0], start_pose['coordinates'][1], 'bv') 
# ax.arrow(start_pose['coordinates'][0], start_pose['coordinates'][1],
#          0.3 * np.cos(start_pose['ori_rad']), 
#          0.3 * np.sin(start_pose['ori_rad']),
#          head_width=0.05, head_length=0.1, fc='b', ec='b')
         
# plt.axis('equal')
# plt.show()




# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# from collections import defaultdict

# points2d = [
#   [100001, [-1.9838, -0.116]],
#   [100000, [-1.9838, 1.5575]],
#   [100011, [-1.7849, -0.7349]],
#   [100010, [-1.7849, 1.5749]],
#   [100025, [-1.7783, 0.1479]],
#   [100024, [-1.7783, 1.2893]],
#   [100002, [-1.6344, -0.4655]],
#   [100014, [-1.2982, -0.1292]],
#   [100023, [-0.9274, 1.2893]],
#   [100022, [-0.9274, 1.5575]],
#   [100003, [-0.8537, 0.3149]],
#   [100005, [-0.7382, -0.8399]],
#   [100015, [-0.7382, -0.4526]],
#   [100004, [-0.7382, 0.3149]],
#   [100006, [-0.1875, -0.8399]],
#   [100016, [-0.1875, -0.7705]],
#   [100007, [-0.1875, -0.2099]],
#   [100020, [-0.1134, 1.1651]],
#   [100021, [-0.1134, 1.5575]],
#   [100017, [0.197, -0.2099]],
#   [100012, [0.2099, -0.7349]],
#   [100013, [0.2099, 1.5749]],
#   [100008, [0.2362, -0.2099]],
#   [100018, [0.2362, -0.142]],
#   [100019, [0.2362, 1.1651]],
#   [100009, [0.2362, 1.5575]]
# ]

# borders = [
#   [0, [100000, 100001, 100002, 100003, 100004, 100005, 100006, 100007, 100008, 100009, 100000]]
# ]

# # Create a mapping from ids to coordinates for easy access
# id_to_coords = {id: coords for id, coords in points2d}

# # Create figure and axes
# fig, ax = plt.subplots()

# # Plot each point
# for id, coords in points2d:
#     ax.scatter(*coords)

# # Plot each border
# for id, border_ids in borders:
#     # Get the coordinates corresponding to each border ID
#     border_coords = [id_to_coords[id] for id in border_ids]

#     # Create the polygon
#     polygon = patches.Polygon(border_coords, fill=False)



# aggregate_floor_type = {
#     "floor_type": "carpet",
#     "geometry": [
#         [
#             [-1.2981, -0.1293],
#             [-1.7784, 0.1479],
#             [-1.7784, 1.2894],
#             [-0.9274, 1.2894],
#             [-0.9274, 1.5575],
#             [-0.1134, 1.5575],
#             [-0.1134, 1.1651],
#             [0.2362, 1.1651],
#             [0.2362, -0.1421],
#             [0.197, -0.2099],
#             [-0.1874, -0.2099],
#             [-0.1874, -0.7705],
#             [-0.7382, -0.4525],
#             [-0.7382, 0.3149],
#             [-0.8538, 0.3149],
#             [-1.2981, -0.1293]
#         ]
#     ]
# }

# # Plot floor type regions
# for region in aggregate_floor_type["geometry"]:
#     # Create the polygon
#     polygon = patches.Polygon(region, color='lightgrey' if aggregate_floor_type["floor_type"] == 'carpet' else 'white', alpha=0.5)
    
#     # Add the polygon to the plot
#     ax.add_patch(polygon)

#     # Add the polygon to the plot
#    # ax.add_patch(polygon)

# # Display the plot
# plt.show()


import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

points2d = {
    100001: [-1.9838, -0.116],
    100000: [-1.9838, 1.5575],
    100011: [-1.7849, -0.7349],
    100010: [-1.7849, 1.5749],
    100025: [-1.7783, 0.1479],
    100024: [-1.7783, 1.2893],
    100002: [-1.6344, -0.4655],
    100014: [-1.2982, -0.1292],
    100023: [-0.9274, 1.2893],
    100022: [-0.9274, 1.5575],
    100003: [-0.8537, 0.3149],
    100005: [-0.7382, -0.8399],
    100015: [-0.7382, -0.4526],
    100004: [-0.7382, 0.3149],
    100006: [-0.1875, -0.8399],
    100016: [-0.1875, -0.7705],
    100007: [-0.1875, -0.2099],
    100020: [-0.1134, 1.1651],
    100021: [-0.1134, 1.5575],
    100017: [0.197, -0.2099],
    100012: [0.2099, -0.7349],
    100013: [0.2099, 1.5749],
    100008: [0.2362, -0.2099],
    100018: [0.2362, -0.142],
    100019: [0.2362, 1.1651],
    100009: [0.2362, 1.5575]
}

borders = [
    {
        "free_type": "free",
        "geometry": {
            "ids": [[100000, 100001, 100002, 100003, 100004, 100005, 100006, 100007, 100008, 100009, 100000]],
            "type": "polygon"
        },
        "id": 0
    }
]


regions = [
    {
        "floor_type": "carpet",
        "geometry": {
            "ids": [[100001, 100002, 100003, 100004, 100005]],
            "type": "polygon"
        },
        "id": 0
    },
    # Add more regions as necessary
]

floor_type_colors = {
    "carpet": "tan",
    # Add more floor types and corresponding colors as necessary
}



poses2d = [
    {
        "coordinates": [-0.0485, 0.0313],
        "id": 100001,
        "ori_rad": -1.0362
    },
    {
        "coordinates": [0, 0],
        "id": 100000,
        "ori_rad": 0
    }
]

typed_poses = {
    "dock_poses": {
        "geometry": {
            "ids": []
        },
        "type": "multipose"
    },
    "end_pose": {
        "geometry": {
            "ids": [100001]
        },
        "type": "multipose"
    },
    "start_pose": {
        "geometry": {
            "ids": [100000]
        },
        "type": "multipose"
    }
}

pose_data = {
    "type": "pose2d_concise",
    "list": [[0.3185, 3.3856, 1.6119]]
}
converted_pose = {
    'coordinates': pose_data['list'][0][:2],
    'ori_rad': pose_data['list'][0][2]
}

poses2d = [converted_pose]


def plot_map(points2d, borders, poses2d):
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

    for id in start_pose_ids:
        x, y = points2d[id]
        ax.plot(x, y, 'go')  # start poses in green

    for id in end_pose_ids:
        x, y = points2d[id]
        ax.plot(x, y, 'ro')  # end poses in red

    for id in dock_pose_ids:
        x, y = points2d[id]
        ax.plot(x, y, 'bo')  # dock poses in blue

    ax.set_aspect('equal', adjustable='datalim')
    plt.show()

plot_map(points2d, borders, poses2d)


