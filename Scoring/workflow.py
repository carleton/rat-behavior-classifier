import tkinter.filedialog as fd
import tempfile, sys
import dlc, dlc_to_jaaba, jaaba 



def workflow():
    video_folder = fd.askdirectory()

    with tempfile.TemporaryDirectory() as tmp_dlc_outputs:
        dlc.get_positions(video_folder, tmp_dlc_outputs)
        dlc_to_jaaba.convert()
        jaaba.get_scores()

