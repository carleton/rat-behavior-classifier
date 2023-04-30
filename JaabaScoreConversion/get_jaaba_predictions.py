import matlab.engine, os

root = os.path.dirname(os.path.realpath(__file__))
os.chdir(root)

eng = matlab.engine.start_matlab()
# Add path to JAABA so that engine has access to JAABA functions
eng.addpath('/Users/neurostudent/Documents/MeertsLabMachineLearning/JAABA/perframe')

experiments_to_predict = '/Users/neurostudent/Documents/MeertsLabMachineLearning/RatExperiment1/TrackConversion/ExperimentDirectory'

# iterate over separate experiment folders https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
for experiment in [f.path for f in os.scandir(experiments_to_predict) if f.is_dir()]:
    eng.JAABADetect(
        experiment,
        'jablistfile',
        os.path.abspath('./jab_list.txt'),
        nargout=0
    )