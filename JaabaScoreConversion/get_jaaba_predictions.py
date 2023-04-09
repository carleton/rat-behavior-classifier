import matlab.engine, os

root = os.path.dirname(os.path.realpath(__file__))
os.chdir(root)

eng = matlab.engine.start_matlab()
# Add path to JAABA so that engine has access to JAABA functions
eng.addpath('/Users/neurostudent/Documents/MeertsLabMachineLearning/JAABA/perframe')

experiment_to_predict = '/Users/neurostudent/Documents/MeertsLabMachineLearning/RatExperiment1/TrackConversion/TestExperiment'

ans = eng.JAABADetect(
    experiment_to_predict,
    'jablistfile',
    os.path.abspath('./jab_list.txt')
)
print(ans)