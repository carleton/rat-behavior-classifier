from numpy.core.records import fromarrays
from scipy.io import savemat, loadmat
import csv
import numpy as np
import cv2
import math
import os

# Returns distance between two coordinates
def lengthFinder(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

# Returns average of given coordinates
def getCenter(positions):
    total, count = 0, 0
    for position in [pos for pos in positions if pos is not None]:
        count += 1
        total += position
    if count == 0:
        return float('nan')

    return total / count

def getTracks(track_list, offset):
    x = []
    y = []
    a_list = []
    b_list = []

    # 4 because of headers in CSV
    theta_list = []
    for row in track_list[4:]:
        nose_x = float(row[1 + offset]) if row[1 + offset] else None
        nose_y = float(row[2 + offset]) if row[2 + offset] else None
        leftear_x = float(row[4 + offset]) if row[4 + offset] else None
        leftear_y = float(row[5 + offset]) if row[5 + offset] else None
        rightear_x = float(row[7 + offset]) if row[7 + offset] else None
        rightear_y = float(row[8 + offset]) if row[8 + offset] else None
        tailbase_x = float(row[10 + offset]) if row[10 + offset] else None
        tailbase_y = float(row[11 + offset]) if row[11 + offset] else None

        x_element = getCenter([nose_x, leftear_x, rightear_x, tailbase_x])
        y_element = getCenter([nose_y, leftear_y, rightear_y, tailbase_y])
        x.append(float(x_element))
        y.append(float(y_element))

        new_value_flag = math.isnan(x_element) or math.isnan(y_element)

        if nose_x and nose_y and tailbase_x and tailbase_y:
            a_list.append(float(lengthFinder(nose_x, nose_y, tailbase_x, tailbase_y) / 4)) 
        else:
            a_list.append(float("nan"))

        if leftear_x and leftear_y and rightear_x and rightear_y:
            b_list.append(float(lengthFinder(leftear_x, leftear_y, rightear_x, rightear_y) / 4)) 
        else:
            b_list.append(float("nan"))

        if new_value_flag:
            theta_list.append(float(0))
        else:
            theta_list.append(float("nan"))

    return x, y, a_list, b_list, theta_list

def main(videoPath, csv_file_path):
    cap = cv2.VideoCapture(videoPath)

    fps = float(cap.get(cv2.CAP_PROP_FPS))
    dt = float(1 / fps)
    print(fps)
    print(dt)

    #read csv
    with open(csv_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        list_csv_reader = list(csv_reader)

        male_x, male_y, male_a, male_b, male_theta = getTracks(list_csv_reader, 0)
        female_x, female_y, female_a, female_b, female_theta = getTracks(list_csv_reader, 12)

    assert len(male_x) == len(male_y) == len(male_a) == len(male_b) == len(female_x) == len(female_y) == len(female_a) == len(female_b)

    nframes = float(len(male_x))

    dt_list = [dt] * int((nframes - 1))

    #write mat struct
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

    mat_file = loadmat('template_trx.mat')

    transposed = np.transpose([list(male_trx_dict.values()), list(female_trx_dict.values())])
    mat_file["trx"] = fromarrays(transposed, names = list(male_trx_dict.keys()))

    savemat(f'{os.path.basename(videoPath).split(".")[0].replace("(", "").replace(")", "").replace(" ", "")}Trx.mat', mat_file)


#36 Optimus Progesterone Dose (1).mp4
#36 Optimus Progesterone DoseDLC_resnet50_RatLabTest3Aug2shuffle1_44500_el_filtered (1).csv

if __name__ == "__main__":
    main("36 Optimus Progesterone Dose.mp4", "36 Optimus Progesterone DoseDLC_resnet50_RatLabTest3Aug2shuffle1_44500_el_filtered.csv")