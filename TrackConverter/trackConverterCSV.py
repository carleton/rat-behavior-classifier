from sys import exc_info
from numpy.core.records import fromarrays
from scipy.io import savemat, loadmat
import csv
import numpy as np
import cv2
import math
import os
import pandas

# Returns distance between a (x,y) coordinate pair
def lengthFinder(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

# Returns average of the given coordinates. If none of them have a value, return NaN. 
def getCenter(positions):
    total, count = 0, 0
    for position in [pos for pos in positions if pos is not None]:
        count += 1
        total += position
    if count == 0:
        return float('nan')
    return total / count

# returns properly formatted tracks for a given animal
def getTracks(track_list, offset):
    x = [] # holds list of x coordinate values
    y = [] # holds list of y coordinate values
    a_list = [] # holds list of "a" coordinate values (a = 1/4 of major axis length)
    b_list = [] # holds list of "b" coordinate values (a = 1/4 of minor axis length)
    theta_list = [] # holds list of theta values (currently just putting NaN if nothing is found within that frame, 0 otherwise.)
    
    # this loop iterates n times, where n = number of frames in the video
    for row in track_list:
        # these variables get the data from the CSV and name them. "offset" is used to get the appropriate data for the sex of the animal(in this case, 
        # it's 0 if male, 12 if female)
        nose_x = float(row[1 + offset]) if not math.isnan(row[1 + offset]) else None
        nose_y = float(row[2 + offset]) if not math.isnan(row[2 + offset]) else None
        leftear_x = float(row[3 + offset]) if not math.isnan(row[3 + offset]) else None
        leftear_y = float(row[4 + offset]) if not math.isnan(row[4 + offset]) else None
        rightear_x = float(row[5 + offset]) if not math.isnan(row[5 + offset]) else None
        rightear_y = float(row[6 + offset]) if not math.isnan(row[6 + offset]) else None
        cervical_x = float(row[7 + offset]) if not math.isnan(row[7 + offset]) else None
        cervical_y = float(row[8 + offset]) if not math.isnan(row[8 + offset]) else None
        shoulder_x = float(row[9 + offset]) if not math.isnan(row[9 + offset]) else None
        shoulder_y = float(row[10 + offset]) if not math.isnan(row[10 + offset]) else None
        thoracic_x = float(row[11 + offset]) if not math.isnan(row[11 + offset]) else None
        thoracic_y = float(row[12 + offset]) if not math.isnan(row[12 + offset]) else None
        hips_x = float(row[13 + offset]) if not math.isnan(row[13 + offset]) else None
        hips_y = float(row[14 + offset]) if not math.isnan(row[14 + offset]) else None
        lumbar_x = float(row[15 + offset]) if not math.isnan(row[15 + offset]) else None
        lumbar_y = float(row[16 + offset]) if not math.isnan(row[16 + offset]) else None
        tail_base_x = float(row[17 + offset]) if not math.isnan(row[17 + offset]) else None
        tail_base_y = float(row[18 + offset]) if not math.isnan(row[18 + offset]) else None
        tail_1_x = float(row[19 + offset]) if not math.isnan(row[19 + offset]) else None
        tail_1_y = float(row[20 + offset]) if not math.isnan(row[20 + offset]) else None
        tail_2_x = float(row[21 + offset]) if not math.isnan(row[21 + offset]) else None
        tail_2_y = float(row[22 + offset]) if not math.isnan(row[22 + offset]) else None
        tail_tip_x = float(row[23 + offset]) if not math.isnan(row[23 + offset]) else None
        tail_tip_y = float(row[24 + offset]) if not math.isnan(row[24 + offset]) else None

        # gets a list of all the x-coordinates for this frame that are not NaN
        x_elements = [
            x_elem for x_elem in [
                nose_x,
                leftear_x,
                rightear_x,
                cervical_x,
                shoulder_x,
                thoracic_x,
                hips_x,
                lumbar_x,
                tail_base_x
            ] if x_elem is not None]

        # gets the x-coordinate of the tail part closest to the rat's body and appends it to the previous list
        priority_tail = [tail_var for tail_var in [tail_1_x, tail_2_x, tail_tip_x] if tail_var is not None]
        if len(priority_tail) > 0:
            x_elements.append(priority_tail[0])

        # gets a list of all the y-coordinates for this frame that are not NaN
        y_elements = [
            y_elem for y_elem in [
                nose_y,
                leftear_y,
                rightear_y,
                cervical_y,
                shoulder_y,
                thoracic_y,
                hips_y,
                lumbar_y,
                tail_base_y
            ] if y_elem is not None]

        # gets the y-coordinate of the tail part closest to the rat's body and appends it to the previous list
        priority_tail = [tail_var for tail_var in [tail_1_y, tail_2_y, tail_tip_y] if tail_var is not None]
        if len(priority_tail) > 0:
            y_elements.append(priority_tail[0])

        # these rows calculate the "center" from the coordinates that are visible in the frame and append it to the appropriate list
        x_element = getCenter(x_elements) 
        y_element = getCenter(y_elements)
        x.append(float(x_element))
        y.append(float(y_element))

        # boolean flag that determines whether we should add 0 or NaN to theta_list. 
        new_value_flag = math.isnan(x_element) or math.isnan(y_element) 

        if new_value_flag:
            theta_list.append(float(0))
        else:
            theta_list.append(float("nan"))
            
        # appends to a_list if the necessary coordinates are found in the frame
        if nose_x and nose_y and tail_base_x and tail_base_y:
            a_list.append(float(lengthFinder(nose_x, nose_y, tail_base_x, tail_base_y) / 4)) 
        else:
            a_list.append(float("nan"))

        # appends to b_list if the necessary coordinates are found in the frame
        if leftear_x and leftear_y and rightear_x and rightear_y:
            b_list.append(float(lengthFinder(leftear_x, leftear_y, rightear_x, rightear_y) / 4)) 
        else:
            b_list.append(float("nan"))

    return x, y, a_list, b_list, theta_list

def csv_to_mat(videoPath, csv_file_path, save_path):
    cap = cv2.VideoCapture(videoPath) # used to get fps of video

    fps = float(cap.get(cv2.CAP_PROP_FPS))
    dt = float(1 / fps) # time between frames, which is simply 1 / fps

    data: pandas.DataFrame = pandas.read_csv(csv_file_path)

    list_data = data.to_numpy().tolist()

    male_x, male_y, male_a, male_b, male_theta = getTracks(list_data, 0) # gets male tracks
    female_x, female_y, female_a, female_b, female_theta = getTracks(list_data, 24) # gets female tracks

    # check to make sure that all lists are equal length(which is necessary for JAABA)
    assert len(male_x) == len(male_y) == len(male_a) == len(male_b) == len(female_x) == len(female_y) == len(female_a) == len(female_b)

    nframes = float(len(male_x)) # nframes is the same for both animals

    dt_list = [dt] * int((nframes - 1)) # time between frames is also the same

    # create the final matlab struct, which is a list of dictionaries(whose fields hold all the tracks)
    trx_array = []
    male_trx_dict = {
        "x" : male_x,
        "y" : male_y,
        "theta" : male_theta,
        "a" : male_a,
        "b" : male_b,
        "nframes" : nframes,
        "firstframe" : float(1),
        "endframe" : nframes,
        "off" : float(0),
        "id" : float(1),
        "x_mm" :  male_x,
        "y_mm" : male_y,
        "theta_mm" : male_theta,
        "a_mm": male_a, 
        "b_mm": male_b,
        "sex" : "m", 
        "dt": dt_list, 
        "fps" : fps
    }
    # this makes sure that the values of all fields(except for sex) are of type float, which is necessary for JAABA
    for val in male_trx_dict.values():
        if val == "m":
            continue
        if type(val) == list:
            val = val[0]
        assert type(val) == float

    female_trx_dict = {
        "x" : female_x,
        "y" : female_y,
        "theta" : female_theta,
        "a" : female_a,
        "b" : female_b,
        "nframes" : nframes,
        "firstframe" : float(1),
        "endframe" : nframes,
        "off" : float(0),
        "id" : float(2),
        "x_mm" :  female_x,
        "y_mm" : female_y,
        "theta_mm" : female_theta,
        "a_mm": female_a, 
        "b_mm": female_b,
        "sex" : "f", 
        "dt": dt_list, 
        "fps" : fps
    }
    trx_array.append(male_trx_dict)
    trx_array.append(female_trx_dict)

    script_location = os.path.dirname(os.path.realpath(__file__))
    mat_file = loadmat(os.path.join(script_location, 'template_trx.mat')) # loads in template mat file

    transposed = np.transpose([list(male_trx_dict.values()), list(female_trx_dict.values())]) # transpose to orient them correctly within MATLAB
    mat_file["trx"] = fromarrays(transposed, names = list(male_trx_dict.keys())) # replace the "trx" fields within this file

    # saves this .mat file locally with a new name
    savemat(os.path.join(save_path, 'p.mat'), mat_file) 

if __name__ == "__main__":
    # replace below with the name of your video and name of the CSV tracks outputted by DeepLabCut
    csv_to_mat("14 Optimus Progesterone Dose.mp4", "14 Optimus Progesterone DoseDLC_dlcrnetms5_RatExperiment1Oct29shuffle1_200000_el.h5")
    pass
