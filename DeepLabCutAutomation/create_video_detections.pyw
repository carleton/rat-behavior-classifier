#!/Users/psycstudent/opt/anaconda3/envs/DEEPLABCUT/bin/ pythonw
# based off of: 
# https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/maDLC_UserGuide.md#optimized-animal-assembly--video-analysis
#
# Run this function to begin the training on the dataset
import deeplabcut, os
from dotenv import load_dotenv, set_key, find_dotenv

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

def main():
    CONFIG_PATH = None

    # Getting the config file path saved in the directory
    with open('CONFIG_PATH.txt', 'r') as config_path_file:
        CONFIG_PATH = config_path_file.read()

    # Evaluate our model
    if os.getenv('evaluation_is_done'):
        scorername = deeplabcut.analyze_videos(CONFIG_PATH,['/Users/psycstudent/Documents/MeertsLabMachineLearning/RatExperiment1/Videos/14 Optimus Progesterone Dose.mp4'], videotype='.mp4')
        deeplabcut.create_video_with_all_detections(CONFIG_PATH, ['/Users/psycstudent/Documents/MeertsLabMachineLearning/RatExperiment1/Videos/14 Optimus Progesterone Dose.mp4'], videotype='.mp4')

# Checks that the previos step is done to prevent running accidentally running this step early
if os.getenv('evaluation_is_done'):
    main()

