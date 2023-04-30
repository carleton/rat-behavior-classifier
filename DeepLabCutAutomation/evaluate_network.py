# based off of: 
# https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/maDLC_UserGuide.md#optimized-animal-assembly--video-analysis
#
# Run this function to begin the training on the dataset
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

    # Evaluate our model    
    if os.getenv('training_is_done'):
        #deeplabcut.evaluate_network(CONFIG_PATH, plotting="individual")
        #set_key(dotenv_file, 'evaluation_is_done', 'True')
        #scorername = deeplabcut.analyze_videos(CONFIG_PATH,['/Users/psycstudent/Documents/MeertsLabMachineLearning/RatExperiment1/RatExperiment1-Sarah Meerts-2021-10-29/videos/14 Optimus Progesterone Dose.mp4'], videotype='.mp4')
        # deeplabcut.create_video_with_all_detections(CONFIG_PATH, ['/Users/psycstudent/Documents/MeertsLabMachineLearning/RatExperiment1/Videos/14 Optimus Progesterone Dose.mp4'], videotype='.mp4')
        #deeplabcut.convert_detections2tracklets(CONFIG_PATH, ['/Users/psycstudent/Documents/MeertsLabMachineLearning/RatExperiment1/RatExperiment1-Sarah Meerts-2021-10-29/videos/14 Optimus Progesterone Dose.mp4'], videotype='mp4', shuffle=1, trainingsetindex=0, identity_only = True)
        # deeplabcut.utils.make_labeled_video.create_video_from_pickled_tracks("/Users/psycstudent/Documents/MeertsLabMachineLearning/RatExperiment1/RatExperiment1-Sarah Meerts-2021-10-29/videos/14 Optimus Progesterone Dose.mp4", "/Users/psycstudent/Documents/MeertsLabMachineLearning/RatExperiment1/RatExperiment1-Sarah Meerts-2021-10-29/videos/14 Optimus Progesterone DoseDLC_dlcrnetms5_RatExperiment1Oct29shuffle1_200000_assemblies.pickle")
        deeplabcut.stitch_tracklets(CONFIG_PATH, ['/Users/psycstudent/Documents/MeertsLabMachineLearning/RatExperiment1/RatExperiment1-Sarah Meerts-2021-10-29/videos/14 Optimus Progesterone Dose.mp4'], videotype='mp4',
                            shuffle=1, trainingsetindex=0)
        # deeplabcut.refine_tracklets("/Users/psycstudent/Documents/MeertsLabMachineLearning/RatExperiment1/RatExperiment1-Sarah Meerts-2021-10-29/config.yaml", "/Users/psycstudent/Documents/MeertsLabMachineLearning/RatExperiment1/RatExperiment1-Sarah Meerts-2021-10-29/videos/14 Optimus Progesterone DoseDLC_dlcrnetms5_RatExperiment1Oct29shuffle1_200000_el.h5", "/Users/psycstudent/Documents/MeertsLabMachineLearning/RatExperiment1/RatExperiment1-Sarah Meerts-2021-10-29/videos/14 Optimus Progesterone Dose.mp4", max_gap=0, min_swap_len=2, min_tracklet_len=2, trail_len=50)
        # deeplabcut.find_outliers_in_raw_data(CONFIG_PATH, "/Users/psycstudent/Documents/MeertsLabMachineLearning/RatExperiment1/RatExperiment1-Sarah Meerts-2021-10-29/videos/14 Optimus Progesterone DoseDLC_dlcrnetms5_RatExperiment1Oct29shuffle1_200000_full.pickle", "/Users/psycstudent/Documents/MeertsLabMachineLearning/RatExperiment1/RatExperiment1-Sarah Meerts-2021-10-29/videos/14 Optimus Progesterone Dose.mp4")
# Checks that the previos step is done to prevent running accidentally running this step early
if os.getenv('training_is_done'):
    main()