import os, shutil
from trackConverterCSV import csv_to_mat

## TODO Change from using first behavior to making a a generic ExperimentDirectory folder which can be copied from if needed

behaviors = ["Mount", "Intros", "Ejac"] # SPECIFY DESIRED BEHAVIORS HERE

FILE_NAME = 0
MOVIE_PATH = 0
CSV_PATH = 1

script_location = os.path.dirname(os.path.realpath(__file__))

project_dir_path = os.path.join(script_location, behaviors[0])

if os.path.exists(project_dir_path):
    shutil.rmtree(project_dir_path)

os.mkdir(project_dir_path)
os.chdir(project_dir_path)

name_to_path = dict()

for file in [f for f in os.listdir("../../Videos") if f.endswith(".mp4")]:
    name_to_path[os.path.splitext(file)[FILE_NAME]] = [os.path.abspath(os.path.join("../../Videos", file))]

for file in [f for f in os.listdir("../../Videos") if f.endswith(".csv")]:
    for key in name_to_path.keys():
        if file.startswith(key):
            name_to_path[key].append(os.path.abspath(os.path.join("../../Videos", file)))

for key, value in name_to_path.items():
    experiment_dir_path = os.path.join(project_dir_path, key)
    movie_path = value[MOVIE_PATH]
    assert(movie_path.endswith(".mp4"))
    os.mkdir(experiment_dir_path)
    shutil.copyfile(movie_path, os.path.join(experiment_dir_path, "movie.mp4"))
    # print(movie_path)
    # print(value[CSV_PATH])
    # print(experiment_dir_path)
    csv_to_mat(movie_path, value[CSV_PATH], experiment_dir_path)

for behavior in behaviors[1:]:
    shutil.copytree(project_dir_path, os.path.join(script_location, behavior))