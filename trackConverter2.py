from numpy.core.records import fromarrays
from scipy.io import savemat, loadmat
import csv
import numpy as np
import cv2
import math
import os

#36 Optimus Progesterone Dose (1).mp4
#36 Optimus Progesterone DoseDLC_resnet50_RatLabTest3Aug2shuffle1_44500_el_filtered (1).csv

videoPath = input("path_to_video: ")

cap = cv2.VideoCapture(videoPath)

fps = cap.get(cv2.CAP_PROP_FPS)

# Returns distance between two coordinates
def lengthFinder(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

# Returns average of given coordinates
def getCenter(positions):
    total, count = 0, 0
    for position in [pos for pos in positions if pos is not None]:
        count += 1
        total += position
    return total / count

def getTracks(firstframe, track_list, offset):
    x = []
    y = []
    dt_list = []
    dt = 1
    a_list = []
    b_list = []

    for row in track_list[firstframe:]:
        nose_x = float(row[1 + offset]) if row[1 + offset] else None
        nose_y = float(row[2 + offset]) if row[2 + offset] else None
        leftear_x = float(row[4 + offset]) if row[4 + offset] else None
        leftear_y = float(row[5 + offset]) if row[5 + offset] else None
        rightear_x = float(row[7 + offset]) if row[7 + offset] else None
        rightear_y = float(row[8 + offset]) if row[8 + offset] else None
        tailbase_x = float(row[10 + offset]) if row[10 + offset] else None
        tailbase_y = float(row[11 + offset]) if row[11 + offset] else None

        try:
            x_element = getCenter([nose_x, leftear_x, rightear_x, tailbase_x])
            y_element = getCenter([ nose_y, leftear_y, rightear_y, tailbase_y])
            x.append(x_element)
            y.append(y_element)
            dt_list.append( dt * (1 / fps))
            dt = 1

            if nose_x and nose_y and tailbase_x and tailbase_y:
                a_list.append(int(lengthFinder(nose_x, nose_y, tailbase_x, tailbase_y) / 4)) 
            else:
                a_list.append(float("nan"))

            if leftear_x and leftear_y and rightear_x and rightear_y:
                b_list.append(int(lengthFinder(leftear_x, leftear_y, rightear_x, rightear_y) / 4)) 
            else:
                b_list.append(float("nan"))

        except ZeroDivisionError:
             dt += 1

    return x, y, dt_list, int(track_list[-1][0]) - dt + 2, a_list, b_list

#read csv
with open(input("path_to_csv: ")) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    list_csv_reader = list(csv_reader)

    male_firstframe = None
    female_firstframe = None

    for row in list_csv_reader[4:]:
        if male_firstframe is None and (row[1] or row[4] or row[7] or row[10]):
            male_firstframe = int(row[0]) + 1
            if female_firstframe:
                break
            
        if female_firstframe is None and (row[13] or row[16] or row[19] or row[22]):
            female_firstframe = int(row[0]) + 1
            if male_firstframe:
                break

    male_x, male_y, male_dt_list, male_endframe, male_a, male_b = getTracks(male_firstframe, list_csv_reader, 0)
    female_x, female_y, female_dt_list, female_endframe, female_a, female_b = getTracks(female_firstframe, list_csv_reader, 12)

male_nframes = len(male_x)
male_placeholder_array = [float("nan")] * male_nframes

female_nframes = len(female_x)
female_placeholder_array = [float("nan")] * female_nframes

#print(len(male_x), len(male_y), len(male_a), len(male_b))
assert len(male_x) == len(male_y) == len(male_a) == len(male_b)

#write mat struct
trx_array = []
male_trx_dict = {
    "x" : male_x,
    "y" : male_y,
    "theta" : male_placeholder_array,
    "a" : male_a,
    "b" : male_b,
    "nframes" : male_nframes,
    "firstframe" : male_firstframe,
    "endframe" : male_endframe,
    "off" : 1 - male_firstframe,
    "id" : 1,
    "x_mm" :  male_placeholder_array,
    "y_mm" : male_placeholder_array,
    "theta_mm" : male_placeholder_array,
    "a_mm": male_placeholder_array, 
    "b_mm": male_placeholder_array,
    "sex" : "M", 
    "dt": male_dt_list, 
    "fps" : fps
}

female_trx_dict = {
    "x" : female_x,
    "y" : female_y,
    "theta" : female_placeholder_array,
    "a" : female_a,
    "b" : female_b,
    "nframes" : female_nframes,
    "firstframe" : female_firstframe,
    "endframe" : female_endframe,
    "off" : 1 - female_firstframe,
    "id" : 2,
    "x_mm" :  female_placeholder_array,
    "y_mm" : female_placeholder_array,
    "theta_mm" : female_placeholder_array,
    "a_mm": female_placeholder_array, 
    "b_mm": female_placeholder_array,
    "sex" : "F", 
    "dt": female_dt_list, 
    "fps" : fps
}
trx_array.append(male_trx_dict)
trx_array.append(female_trx_dict)

mat_file = loadmat('template_trx.mat')
transposed = np.transpose([list(male_trx_dict.values()), list(female_trx_dict.values())])
mat_file["trx"] = fromarrays(transposed, names = list(male_trx_dict.keys()))

savemat(f'{os.path.basename(videoPath).split(".")[0]}_trx.mat', mat_file)
