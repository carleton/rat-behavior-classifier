import matlab.engine, os

# Run this function to convert the generated h5 files to csv's so we can work with them
root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
os.chdir(root)

def get_predictions(experiments_dir, jab_files, output_dir=None):
    eng = matlab.engine.start_matlab()
    # Add path to JAABA so that engine has access to JAABA functions
    eng.addpath('./JAABA/perframe')

    print('h')
    for a in [f for f in os.scandir(experiments_dir)]:
        print(a.path)
    # iterate over separate experiment folders https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
    for experiment in [f for f in os.scandir(experiments_dir) if f.is_dir()]:
        print(experiment)
        eng.JAABADetect(
            experiment.path,
            'jabfiles',
            jab_files,
            nargout=0
        )
    
        if output_dir is not None:
            print('test', output_dir)
            import shutil
            output_path = os.path.join(output_dir, experiment.name)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            for score in [f.path for f in os.scandir(experiment.path) if f.name.startswith('scores_')]:
                print(score, output_path)
                shutil.copy(src=score, dst=output_path)


if __name__ == "__main__":
    get_predictions('./JaabaExperiments/Ejac', os.path.abspath("./JaabaScoreConversion/jab_list.txt"))