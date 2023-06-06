import os, shutil
from trackConverterCSV import csv_to_mat

# Run this function to convert the generated h5 files to csv's so we can work with them
root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
os.chdir(root)

behaviors = ["Mount", "Intros", "Ejac"] # SPECIFY DESIRED BEHAVIORS HERE

FILE_NAME = 0
MOVIE_PATH = 0
CSV_PATH = 1

if os.path.exists("./JaabaExperiments"):
    shutil.rmtree("./JaabaExperiments")

os.mkdir("./JaabaExperiments")
os.mkdir(os.path.join("./JaabaExperiments", behaviors[0]))

name_to_path = dict()

for file in [f for f in os.listdir("./Videos") if f.endswith(".mp4")]:
    name_to_path[os.path.splitext(file)[FILE_NAME]] = [os.path.abspath(os.path.join("./Videos", file))]

for file in [f for f in os.listdir("./Videos") if f.endswith(".csv")]:
    for key in name_to_path.keys():
        if file.startswith(key):
            name_to_path[key].append(os.path.abspath(os.path.join("./Videos", file)))

for key, value in name_to_path.items():
    experiment_dir_path = os.path.join("./JaabaExperiments", behaviors[0], key)
    movie_path = value[MOVIE_PATH]
    assert(movie_path.endswith(".mp4"))
    os.mkdir(experiment_dir_path)
    shutil.copyfile(movie_path, os.path.join(experiment_dir_path, "movie.mp4"))
    csv_to_mat(movie_path, value[CSV_PATH], experiment_dir_path)

for behavior in behaviors[1:]:
    shutil.copytree(os.path.join("./JaabaExperiments", behaviors[0]), os.path.join("./JaabaExperiments", behavior))