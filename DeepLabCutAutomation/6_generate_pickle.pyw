#!/Users/psycstudent/opt/anaconda3/envs/DEEPLABCUT/bin/ pythonw
# based off of: 
# https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/maDLC_UserGuide.md#optimized-animal-assembly--video-analysis
#
# Run this function to begin the training on the dataset
import deeplabcut, os
from dotenv import load_dotenv, find_dotenv, set_key
os.chdir("..")

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

def clean_up_videos_folder():
    abs_path_to_videos = os.path.abspath("./Videos")
    for file in os.listdir(abs_path_to_videos):
        file_abs_path = os.path.join(abs_path_to_videos, file)
        if not file.endswith(".mp4") and not os.path.isdir(file_abs_path):
            # print(file)
            os.remove(file_abs_path)

def main():
    clean_up_videos_folder()
    CONFIG_PATH = None

    # Getting the config file path saved in the directory
    with open('CONFIG_PATH.txt', 'r') as config_path_file:
        CONFIG_PATH = config_path_file.read()

    # Generate h5 file  
    abs_path_to_videos = os.path.abspath("./Videos")
    clean_up_videos_folder()

    deeplabcut.analyze_videos(CONFIG_PATH, [abs_path_to_videos], videotype="mp4", auto_track = False)

    set_key(dotenv_file, 'pickles_generated', 'True')
    
# Checks that the previos step is done to prevent running accidentally running this step early
if os.getenv('training_is_done'):
    main()