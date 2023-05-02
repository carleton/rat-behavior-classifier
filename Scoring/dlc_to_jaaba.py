import sys, os
sys.path.append('../TrackConverter')
import trackConverterCSV as tcc

def convert(video_folder, csv_folder, experiment_folder):
    videos = [vp for vp in os.listdir(video_folder) if os.path.splitext(vp)[1] == '.mp4']
    for video_name in videos:
        video_path = os.path.join(video_folder, video_name)
        csv_name = f'{os.path.splitext(video_name)[0]}.csv'
        csv_path = os.path.join(csv_folder, csv_name)
        tcc.csv_to_mat(video_path, csv_path, experiment_folder)
