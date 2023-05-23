import sys
sys.path.append('./JaabaScoreConversion')
import get_jaaba_predictions as gjp
import score_converter as sc

def get_scores(experiment_folder, behavior_list, output_folder):
    gjp.get_predictions(experiment_folder, behavior_list, output_folder)
    # sc.main()