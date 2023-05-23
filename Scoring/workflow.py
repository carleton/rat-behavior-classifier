import tkinter.filedialog as fd
import tempfile, sys, os
import dlc, dlc_to_jaaba, jaaba



def workflow():
    video_folder = fd.askdirectory(title="Input Videos Folder")

    jab_folder = fd.askdirectory(title="Input JAB (Behaviors) Folder")
    tmp_jab_files = [f.path for f in os.scandir(jab_folder) if f.name.endswith('.jab')]

    with tempfile.TemporaryDirectory() as tmp_csv_outputs, tempfile.TemporaryDirectory() as tmp_experiments:
        dlc.get_positions(video_folder, tmp_csv_outputs)
        dlc_to_jaaba.convert(video_folder, tmp_csv_outputs, tmp_experiments)
        jaaba.get_scores(tmp_experiments, tmp_jab_files, "./Scoring/Outputs")

if __name__ == "__main__":
    workflow()
