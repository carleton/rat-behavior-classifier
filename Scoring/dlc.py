import deeplabcut
import os, sys

# Run this function to convert the generated h5 files to csv's so we can work with them
root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
os.chdir(root)

sys.path.append('./DeepLabCutAutomation')
ptc = __import__('7_dlc_pickle_to_csv')

def get_positions(video_folder, output_dir):
    CONFIG_PATH = None

    # Getting the config file path saved in the directory
    with open('CONFIG_PATH.txt', 'r') as config_path_file:
        CONFIG_PATH = config_path_file.read()
    
    deeplabcut.analyze_videos(CONFIG_PATH, [video_folder], videotype="mp4", auto_track = False)

    for file in os.listdir(video_folder):
        if file.endswith('_full.pickle'):
            ptc.pickle_to_csv(os.path.join(video_folder, file), output_dir)