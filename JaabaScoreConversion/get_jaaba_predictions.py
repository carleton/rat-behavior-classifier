import matlab.engine, os

def get_predictions(experiments_dir):
    eng = matlab.engine.start_matlab()
    # Add path to JAABA so that engine has access to JAABA functions
    eng.addpath('/Users/neurostudent/Documents/MeertsLabMachineLearning/JAABA/perframe')

    # iterate over separate experiment folders https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
    for experiment in [f.path for f in os.scandir(experiments_dir) if f.is_dir()]:
        eng.JAABADetect(
            experiment,
            'jablistfile',
            os.path.abspath('./jab_list.txt'),
            nargout=0
        )

if __name__ == "__main__":
    get_predictions('/Users/neurostudent/Documents/MeertsLabMachineLearning/RatExperiment1/TrackConversion/ExperimentDirectory')