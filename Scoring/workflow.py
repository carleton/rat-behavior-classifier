import tkinter.filedialog as fd
import tempfile, sys, os
import dlc, dlc_to_jaaba, jaaba



def workflow():
    """
    This code imports all the required funcitons and runs the entire workflow for new videos, given that JAABA and DLC are trained
    """

    # Asks for the folder in which the videos to be run through the workflow are located
    video_folder = fd.askdirectory(title="Input Videos Folder")

    # Asks for the folder in which the .jab trained behaviors are located
    jab_folder = fd.askdirectory(title="Input JAB (Behaviors) Folder")
    tmp_jab_files = [f.path for f in os.scandir(jab_folder) if f.name.endswith('.jab')]

    # Create temporary directories to store data of intermediary steps
    with tempfile.TemporaryDirectory() as tmp_csv_outputs, tempfile.TemporaryDirectory() as tmp_experiments:
        # Run the DLC model on each video to get the animal positions
        dlc.get_positions(video_folder, tmp_csv_outputs)
        # Convert from DLC to JAABA experiments
        dlc_to_jaaba.convert(video_folder, tmp_csv_outputs, tmp_experiments)
        # Run the JAABA model on the experiments and place the results in the Outouts folder
        jaaba.get_scores(tmp_experiments, tmp_jab_files, "./Scoring/Outputs")

if __name__ == "__main__":
    workflow()
