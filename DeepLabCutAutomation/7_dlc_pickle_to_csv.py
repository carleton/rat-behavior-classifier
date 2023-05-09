import pickle, re, csv, os
import numpy as np
from dotenv import load_dotenv, find_dotenv, set_key
from dataclasses import dataclass
from typing import Tuple

# Run this function to convert the generated h5 files to csv's so we can work with them
root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
os.chdir(root)

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

Position = Tuple[float, float]

@dataclass(frozen=True)
class Joint:
    pos: Position
    confidence: float = 1.0
    label: int = None
    idx: int = None
    group: int = -1

def _flatten_detections(data_dict):
    ind = 0
    coordinates = data_dict["coordinates"][0]
    confidence = data_dict["confidence"]
    ids = data_dict.get("identity", None)
    if ids is None:
        ids = [np.ones(len(arr), dtype=int) * -1 for arr in confidence]
    else:
        ids = [arr.argmax(axis=1) for arr in ids]
    for i, (coords, conf, id_) in enumerate(zip(coordinates, confidence, ids)):
        if not np.any(coords):
            continue
        for xy, p, g in zip(coords, conf, id_):
            joint = Joint(tuple(xy), p.item(), i, ind, g)
            ind += 1
            yield joint

def pickle_to_csv(pickle_path):
    with open(pickle_path, "rb") as handle:
        pickle_data = pickle.load(handle)

    data = dict(pickle_data)

    header = data.pop("metadata")
    all_jointnames = header["all_joints_names"]
    numjoints = len(all_jointnames)
    len_result = 4*numjoints-3
    bpts = range(numjoints)

    frame_names = list(data)
    frames = [int(re.findall(r"\d+", name)[0]) for name in frame_names]

    with open(pickle_path.replace("_full.pickle", ".csv"), "w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out)
        for n in range(max(frames)):
            result = [""]*len_result
            result[0] = n
            try:
                ind = frames.index(n)
                dets = _flatten_detections(data[frame_names[ind]])
                for det in dets:
                    if det.label not in bpts and det.confidence > 0.6:
                        continue
                    x, y = det.pos
                    if(det.label > 11):
                        index = 51 + (12 - det.label)*2
                    else:
                        index = det.label*2+(det.group*24)+1
                    result[index] = x
                    result[index+1] = y
            except ValueError:  # No data stored for that particular frame
                # print(n, "no data")
                pass
            writer.writerow(result)

if __name__ == "__main__":
    videos_folder_path = os.path.abspath('./Videos')
    for file in os.listdir(videos_folder_path):
        if file.endswith('_full.pickle'):
            pickle_to_csv(os.path.join(videos_folder_path, file))
    set_key(dotenv_file, 'csv_generated', 'True')