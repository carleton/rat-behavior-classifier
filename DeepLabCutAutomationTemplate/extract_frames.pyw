#!/Users/psycstudent/opt/anaconda3/envs/DEEPLABCUT/bin/ pythonw
# based off of: 
# https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/maDLC_UserGuide.md#optimized-animal-assembly--video-analysis
#
# Run this function after a DLC project has been in order to capture more frames to be labeled such as: interesting behavior or
# examples of multi animals in interacting
# Note: You will have to quit and rerun for each seperate video you wish to extract frames from

import deeplabcut

CONFIG_PATH = None

# Getting the config file path saved in the directory
with open('CONFIG_PATH.txt', 'r') as config_path_file:
    CONFIG_PATH = config_path_file.read()

# Launch GUI to extract frames manually.
# Note: You will have to quit and rerun for each separate video you wish to extract frames from
deeplabcut.extract_frames(CONFIG_PATH, 'manual')