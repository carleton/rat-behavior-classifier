#!/Users/psycstudent/opt/anaconda3/envs/DEEPLABCUT/bin/ pythonw
# based off of: 
# https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/maDLC_UserGuide.md#optimized-animal-assembly--video-analysis
# We are assuming that the code will be run in an experimentl directory of the following structure
# ExperimentName (Folder)
#       |
#       ----   Videos (Folder)
#       |             |
#       |             ---- VideoNames.mp4 (May work with other video formats, I do not know)
#       |
#       ----   create_project.pyw (In this file you may want to change the edits dictionary to change the DLC config file)
#       |
#       ----   extract_frames.pyw (Run to extract more frames for DLC)
#       |
#       ----   label_frames.pyw (Run to label frames for DLC)
#
# After the code is run, there will be a new folder created for the DLC project named PROJECT_NAME-Your_Name-YYYY-MM-DD.
# There will also be a CONFIG_PATH.txt file that contains the absolute path of the DLC config file to help with running manual 
# DLC functions.
# New Directory Structure:
# ExperimentName (Folder)
#       |
#       ----   Videos (Folder)
#       |             |
#       |             ---- VideoNames.mp4 (May work with other video formats, I do not know)
#       |
#       ----   PROJECT_NAME-Your_Name-YYYY-MM-DD (DLC Project Folder)
#       |             |
#       |             ---- dlc-model (folder)
#       |             |
#       |             ---- labeled-data (folder)
#       |             |
#       |             ---- training-datasets (folder)
#       |             |
#       |             ---- videos (folder, contains a copy of the videos if copy_videos=True when calling create_new_project)
#       |             |         |
#       |             |         ---- VideoNames.mp4
#       |             |
#       |             ---- config.yaml (DLC config file)
#       |
#       ----   CONFIG_PATH.txt (Text file containing the absolute path to the DLC project's config.yaml file)
#       |
#       ----   create_project.pyw (In this file you may want to change the edits dictionary to change the DLC config file)
#       |
#       ----   extract_frames.pyw (Run to extract more frames for DLC)
#       |
#       ----   label_frames.pyw (Run to label frames for DLC)

import deeplabcut
import os

root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
os.chdir(root)

# Is used to name the DLC project: PROJECT_NAME-Your_Name-YYYY-MM-DD
PROJECT_NAME = "RatExperiment1"
YOUR_NAME = "Sarah Meerts"
os.chdir("Videos")
# Create an array of the absolute paths to all the videos in the Video folder.
videoPathsArray = [os.path.abspath(video) for video in os.listdir() if video.endswith(".mp4")]
os.chdir("..")
# Create a new DLC project.
CONFIG_PATH = deeplabcut.create_new_project(PROJECT_NAME, YOUR_NAME, videoPathsArray, copy_videos=True, multianimal=True)
# Save config file path for future use
with open('CONFIG_PATH.txt', 'w') as config_path_file:
    config_path_file.write(CONFIG_PATH)
# Set up edits to the config file.
edits = {
    "uniquebodyparts": ["topDivider", "bottomDivider"], # Can be objects or animals that will at most appear once in a frame.
    "individuals": ["male", "female"], # Individuals animals.
    "multianimalbodyparts": ["nose",
                            "left_ear",
                            "right_ear",
                            "cervical",
                            "shoulder",
                            "thoracic",
                            "hips",
                            "lumbar",
                            "tail_base",
                            "tail_1",
                            "tail_2",
                            "tail_tip"
                            ], # Body parts of individual animals.
    "skeleton": [
                    ["nose", "left_ear"], 
                    ["nose", "right_ear"], 
                    ["nose", "tail_base"],
                    ["nose", "cervical"],
                    ["cervical", "shoulder"],
                    ["shoulder", "thoracic"],
                    ["thoracic", "hips"],
                    ["hips", "lumbar"],
                    ["lumbar", "tail_base"],
                    ["tail_base", "tail_1"],
                    ["tail_1", "tail_2"],
                    ["tail_2", "tail_tip"]
                ], # Create a connection between a pairs of bodyparts to form a skeleton.
    "identity": True,  # If the animals are distinguishable by eye.
    "numframes2pick": 25 # The number of frames extracted from each video for labeling.
}
# Update the config file with the edits.
deeplabcut.auxiliaryfunctions.edit_config(CONFIG_PATH, edits)
# Extracts frames from all the videos in the config file.
# You can add more videos at any point with the add_new_video function.
# Extracts frames defaults to kmeans in order to select visually different frames.
# WARNING: Kmeans is currently not working so we are using uniform to get the base frames.
# Userfeedback is set to false so that the extraction is automatic for all videos.
deeplabcut.extract_frames(CONFIG_PATH, algo="uniform", userfeedback=False)
