#!/Users/psycstudent/opt/anaconda3/envs/DEEPLABCUT/bin/ pythonw
# based off of: 
# https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/maDLC_UserGuide.md#optimized-animal-assembly--video-analysis
#
# Run this function to begin the trainig on the dataset
import deeplabcut, os
from dotenv import load_dotenv, set_key, find_dotenv
os.chdir("..")

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

def main():
    CONFIG_PATH = None

    # Getting the config file path saved in the directory
    with open('CONFIG_PATH.txt', 'r') as config_path_file:
        CONFIG_PATH = config_path_file.read()

    # Train our model
    deeplabcut.train_network(CONFIG_PATH, allow_growth=True, maxiters = 100000)
    set_key(dotenv_file, 'training_is_done', 'True')

# Checks that the previos step is done to prevent running accidentally running this step early
if os.getenv('dataset_created'):
    main()