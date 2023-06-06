import sys

# Import our JAABA scripts
sys.path.append('./JaabaScoreConversion')
import get_jaaba_predictions as gjp
import score_converter as sc

def get_scores(experiment_folder, behavior_list, output_folder):
    # Run the JAABA model of each provided behavior on the experiments
    gjp.get_predictions(experiment_folder, behavior_list, output_folder)

    # TODO Convert the JAABA output into the ChamberMate csv structure
    # sc.main()