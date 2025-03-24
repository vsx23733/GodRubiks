import numpy as np
import cv2 
import time
from helpers import ciede2000, bgr2lab

cv2.namedWindow(winname="Rubiks Cube Numerizer")
start_time = time.time()
webacm = cv2.VideoCapture(0)


if webacm.isOpened():
    rval, frame = webacm.read()  

else :
    rval = False

color_ranges = {
    'blue': {
        'lower': [128, 0, 0],     # Dark Blue (low intensity)
        'upper': [255, 100, 100]      # Bright Blue
    },
    'red': {
        'lower': [0, 0, 128],     # Dark Red
        'upper': [100, 100, 255]      # Bright Red
    },
    'green': {
        'lower': [0, 128, 0],     # Dark Green
        'upper': [100, 255, 100]      # Bright Green
    },
    'yellow': {
        'lower': [0, 128, 128],   # Dark Yellow
        'upper': [100, 255, 255]    # Bright Yellow
    },
    'orange': {
        'lower': [0, 100, 200],   # Dark Orange
        'upper': [100, 165, 255]    # Bright Orange
    },
    'white': {
        'lower': [200, 200, 200], # Off White
        'upper': [255, 255, 255]  # Pure White
    }
}

def get_dominant_color(roi):
        """
        Get dominant color from a certain region of interest.

        :param roi: The image list.
        :returns: tuple
        """
        pixels = np.float32(roi.reshape(-1, 3))

        n_colors = 1
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)
        dominant = palette[np.argmax(counts)]
        return tuple(dominant)


while rval:

    cv2.imshow("feed", frame)
    rval, frame = webacm.read()
    width, height, _ = frame.shape
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    start_x = int((width/2))
    start_y =  int((height/4))
    square_size = 5
    spacing = 25

    
    current_time = time.time()
    elapse_time = current_time - start_time 

    
    detected_colors = []
    color_code_list = []
    cube = [] # Final digitized cube 
    
    
    for i in range (1, 4):

        for j in range(1, 4): 

            pt1_x = start_x + j * (square_size + spacing)  
            pt1_y = start_y + i * (square_size + spacing)  
            
            pt1 = (pt1_x, pt1_y)
            pt2 = (pt1_x + square_size, pt1_y + square_size)

            frame = cv2.rectangle(frame, pt1, pt2, 
                                  color=(255, 0, 0), thickness=1)

            rect_region = frame[pt1[1]:pt2[1], pt1[0]:pt2[0]]

            center_x = pt1[0] + square_size // 2
            center_y = pt1[1] + square_size // 2
            exact_color = frame[center_y, center_x]  

            dominant = get_dominant_color(rect_region)
            
            detected_colors.append(exact_color)  

    if elapse_time >= 30:
        break

    key = cv2.waitKey(delay=10)     
    if key == 27:
        break



row = []

color_centers = {
    'blue': np.array([255, 0, 0]),
    'red': np.array([0, 0, 255]),
    'green': np.array([0, 255, 0]),
    'yellow': np.array([0, 255, 255]), # Dark yellow 
    'orange': np.array([0, 165, 255]), # Bright orange
    'white': np.array([255, 255, 255])
}

def classify_color(bgr_value):
    bgr_value = np.array(bgr_value)
    closest_color = None
    min_distance = float('inf')

    for color, center in color_centers.items():
        distance = np.linalg.norm(bgr_value - center)
        if distance < min_distance:
            min_distance = distance
            closest_color = color

    return closest_color

def get_closest_color(bgr):
        """
        Get the closest color of a BGR color using CIEDE2000 distance.

        :param bgr tuple: The BGR color to use.
        :returns: dict
        """
        lab = bgr2lab(bgr)
        distances = []
        for color_name, color_bgr in color_centers.items():
            distances.append({
                'color_name': color_name,
                'color_bgr': color_bgr,
                'distance': ciede2000(lab, bgr2lab(color_bgr))
            })
        closest = min(distances, key=lambda item: item['distance'])
        return closest

for scalar_color in detected_colors:
    """for color in list(color_ranges.keys()):
        if (color_ranges[color]["lower"][0] <= scalar_color[0] <= color_ranges[color]["upper"][0]) and \
                (color_ranges[color]["lower"][1] <= scalar_color[1] <= color_ranges[color]["upper"][1]) and \
                (color_ranges[color]["lower"][2] <= scalar_color[2] <= color_ranges[color]["upper"][2]):
            row.append(color)            
            break"""

    color_name = get_closest_color(scalar_color)
    row.append(color_name)
 
print(f"\n{detected_colors}\n")
print(f"\n{row}\n")   

cv2.destroyAllWindows()
webacm.release()