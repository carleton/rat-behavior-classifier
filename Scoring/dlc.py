import deeplabcut
import os

def get_positions(video_folder, output_dir):
    CONFIG_PATH = None

    # Getting the config file path saved in the directory
    with open('CONFIG_PATH.txt', 'r') as config_path_file:
        CONFIG_PATH = config_path_file.read()

    video_paths = [os.path.join(video_folder, vp) for vp in os.listdir(video_folder) if os.path.splitext(vp)[1] == '.mp4']
    deeplabcut.analyze_videos(CONFIG_PATH, video_paths, save_as_csv=True, destfolder=output_dir)