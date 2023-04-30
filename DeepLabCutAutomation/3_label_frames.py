# based off of: 
# https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/maDLC_UserGuide.md#optimized-animal-assembly--video-analysis
#
# Run this function to label extracted frames. You will want to select a folder under the labeled-data folder which contains
# sub directories for each video with the extracted frames. Select one video subdirectory, go through and label it 
# (there is a help option in the GUI) and then click save. You can save and quit at any point. Once you press quit it will 
# ask if you want to label another video. Repeat until you are done. You can always quit and run this function another 
# time to continue where you left off as long as you have saved your work.

import deeplabcut, os
from dotenv import load_dotenv, set_key, find_dotenv

root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
os.chdir(root)

with open(".env", "w"):
    pass

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

CONFIG_PATH = None

# Getting the config file path saved in the directory
with open('CONFIG_PATH.txt', 'r') as config_path_file:
    CONFIG_PATH = config_path_file.read()

# Launch GUI to label frames for a multiple animal project
deeplabcut.label_frames(CONFIG_PATH)
# If the labeling is done, sets an environmental variable to make it possible to continue with the next step
# This will prevent running the next step accidentally before this step is done
if (input("If you are done labeling EVERY frame for EVERY video, enter y to enable the next step.\n").casefold() == 'y'): 
    set_key(dotenv_file, 'labeling_is_done', 'True')