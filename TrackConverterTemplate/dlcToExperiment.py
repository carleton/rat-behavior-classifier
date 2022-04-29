import os, shutil
from trackConverterH5 import h5_to_mat

FILE_NAME = 0
MOVIE_PATH = 0
H5_PATH = 1

script_location = os.path.dirname(os.path.realpath(__file__))
project_dir_path = os.path.join(script_location, "ExperimentDirectory")

if os.path.exists(project_dir_path):
    shutil.rmtree(project_dir_path)

os.mkdir(project_dir_path)
os.chdir(project_dir_path)

name_to_path = dict()

for file in [f for f in os.listdir("../../Videos") if f.endswith(".mp4")]:
    name_to_path[os.path.splitext(file)[FILE_NAME]] = [os.path.abspath(os.path.join("../../Videos", file))]

for file in [f for f in os.listdir("../../Videos") if f.endswith(".h5")]:
    for key in name_to_path.keys():
        if file.startswith(key):
            name_to_path[key].append(os.path.abspath(os.path.join("../../Videos", file)))

for key, value in name_to_path.items():
    experiment_dir_path = os.path.join(project_dir_path, key)
    movie_path = value[MOVIE_PATH]
    assert(movie_path.endswith(".mp4"))
    os.mkdir(experiment_dir_path)
    shutil.copyfile(movie_path, os.path.join(experiment_dir_path, "movie.mp4"))
    h5_to_mat(movie_path, value[H5_PATH], experiment_dir_path)