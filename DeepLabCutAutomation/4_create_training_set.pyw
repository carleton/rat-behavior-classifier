#!/Users/psycstudent/opt/anaconda3/envs/DEEPLABCUT/bin/ pythonw
# based off of: 
# https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/maDLC_UserGuide.md#optimized-animal-assembly--video-analysis
#
# Run this function to split up the labeled frames into a training and testing dataset
import deeplabcut, os
from dotenv import load_dotenv, set_key, find_dotenv

root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
os.chdir(root)

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

def main():
    CONFIG_PATH = None

    # Getting the config file path saved in the directory
    with open('CONFIG_PATH.txt', 'r') as config_path_file:
        CONFIG_PATH = config_path_file.read()

    # Create train and test datasets for the machine learning step
    deeplabcut.create_multianimaltraining_dataset(CONFIG_PATH)
    # Sets an environmental variable to make it possible to continue with the next step
    # This will prevent running the next step accidentally before this step is done
    set_key(dotenv_file, 'dataset_created', 'True')

# Check that labeling is done to prevent accidentally this step early.
if os.getenv('labeling_is_done') and not os.getenv('dataset_created'):
    main()
else:
    print("Labeling is not yet done!")