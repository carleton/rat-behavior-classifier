import sys, os, shutil
print(os.getcwd())
sys.path.append('./TrackConverter')
import trackConverterCSV as tcc

def convert(video_folder, csv_folder, experiment_folder):
    videos = [vp for vp in os.listdir(video_folder) if os.path.splitext(vp)[1] == '.mp4']
    csv = [cp for cp in os.listdir(csv_folder) if os.path.splitext(cp)[1] == '.csv']
    print(videos, csv)
    for video_name in videos:
        output_dir = os.path.join(experiment_folder, video_name.replace('.mp4', ''))
        os.mkdir(output_dir)
        
        video_path = os.path.join(video_folder, video_name)
        shutil.copyfile(video_path, os.path.join(output_dir, "movie.mp4"))
        
        csv_name = [cn for cn in csv if cn.startswith(os.path.splitext(video_name)[0])][0]
        csv_path = os.path.join(csv_folder, csv_name)

        tcc.csv_to_mat(video_path, csv_path, output_dir)
