import os
from scipy.io import savemat, loadmat

def select_rat():
    #TODO Give rat selection prompt
    return 1

def get_count(scores):
    num_bouts = 0 # number of times that behavior is identified in the frames

    # TODO determine these variables
    # predetermined variables
    min_bout_length = 5 # bout must exceed this number of frames
    max_bout_length = 30 # bout must be less than this number of frames
    max_none_frames = 5 # bout cannot exceed this number of none frames in a arow

    # variables to track a bout
    cur_bout_length = 0 # number of frames comprising the current bout of behavior
    num_none_frames = 0 # number of frames in a row labeled as none
    tracking_bout = False # currently in the midst of a potential bout

    for frame in scores:
        if not tracking_bout:
            # behavior is predicted to occur, start tracking a potential bout and reset tracking variables
            if frame == 1:
                cur_bout_length = 1
                tracking_bout = True
                num_none_frames = 0
        else:
            # behavior is predicted to occur, increment length of current bout and set num_none_frames to 0
            if frame == 1:
                cur_bout_length += 1
                num_none_frames = 0
            
            # behavior is predicted to not occur(either NaN or 0), so increment number of none frames. 
            else:
                num_none_frames += 1
                # If it exceeds a threshold, consider it as the end of the bout.
                if num_none_frames >= max_none_frames:
                    tracking_bout = False 
                    # if the bout is within the acceptable range of behavior length, increment the number of bouts
                    if min_bout_length < cur_bout_length < max_bout_length:
                        num_bouts += 1
    print(num_bouts)

def chambermate_format():
    #TODO reformat data to match chambermate data and output it 
    pass

def main():
    raw_scores = loadmat(os.path.join('/Users/neurostudent/Downloads/', 'test.mat'))
    raw_scores = list(raw_scores['allScores']['postprocessed'][0][0][0][select_rat()][0])
    print(type(raw_scores))
    # print(len(raw_scores[0]))
    # for index, row in enumerate(raw_scores):
    #     print(index, row)
    clean_scores = get_count(raw_scores)
    # chambermate_format(clean_scores)

if __name__ == "__main__":
    main()