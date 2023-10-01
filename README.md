# MeertsLabMachineLearning

## Introduction
This is a project is that uses DeepLabCut and JAABA to classify animal behavior. The idea is that we use DeepLabCut as a non-invasive multi-part tracker to get the tracks of the animals and then we feed those tracks into JAABA to train behavior classifiers that will then be able to predict bouts of animal behavior on new videos.

DeepLabCut documentation: https://deeplabcut.github.io/DeepLabCut/README.html

JAABA documentation: https://jaaba.sourceforge.net/

## Getting Ready
We recommend installing [VS Code](https://code.visualstudio.com/download) and [git](https://git-scm.com/download) in order to clone the code and run it locally.

You will need [Anaconda](https://www.anaconda.com/download/) to run DeepLabCut and Matlab to run JAABA.

### Submodule Setup
To run DeepLabCut and JAABA we must download the source code. In a terminal, navigate to this project and run the following command:

```console
git submodule update --init
```

### DeepLabCut Setup
<!--
Is not working at the moment

With the code downloaded and Anaconda installed, you will then have to open up the terminal and navigate to [DeepLabCut/conda-environments](./DeepLabCut/conda-environments) folder. If you open this project in VS Code and open a terminal you simply need to run the following commands.

cd DeepLabCut/conda-environments        # navigate to the correct folder
conda env create -f DEEPLABCUT.yaml     # install the DeepLabCut Anaconda environment (dependencies)
-->

With the code downloaded and Anaconda installed, you will then have to set up the conda environmet by running the following commands in the terminal.
```console
conda create -n DEEPLABCUT python=3.10
conda activate DEEPLABCUT
conda install -y -q python-dotenv
pip install "deeplabcut[tf,gui]"
```

In the [rat-behavior-classifier folder](.), you must create a folder named Videos within which you place the video (.mp4) of each experiment you will be using to train the model.

Before you begin you will need to open [DeepLabCutAutomation/1_create_project.pyw](./DeepLabCutAutomation/1_create_project.pyw) an adjust the ```PROJECT_NAME```, ```YOUR_NAME``` and ```edits``` to your specific project requirements.

### JAAAB Setup
JAABA requires the JAABA code (see [Submodule Setup](#submodule-setup)) and MatLab to be installed as well as the MatLab toolboxes:
- Parallel Computing Toolbox
- Image Processing Toolbox

## What is DeepLabCut?

DeepLabCut is a library that allows one to train deep neural networks to track the body parts of one or more animals by labeling a small number of frames. Read more about it here: http://www.mackenziemathislab.org/deeplabcut#:~:text=DeepLabCut%E2%84%A2%20is%20an%20efficient,typically%2050%2D200%20frames).

Read our DeepLabCut.md file for more details.

## What is JAABA?

- JAABA is a library that allows one to train animal behavior classifiers by giving it tracks of animal body parts(obtained through DeepLabCut in our case) and labeling a small number of the behavior occurring within a video. The official description is below:

    "JAABA is a machine learning-based system that enables researchers to automatically compute interpretable, quantitative statistics describing video of behaving animals. Through our system, users encode their intuition about the structure of behavior by labeling the behavior of the animal, e.g. walking, grooming, or following, in a small set of video frames. JAABA uses machine learning techniques to convert these manual labels into behavior detectors that can then be used to automatically classify the behaviors of animals in large data sets."

- Here are some Google docs that we have written with more information: 
    - JAABA 101: https://docs.google.com/document/d/1cxoGsuiK8lHuTF_r5S5VBk25jN60DtfTjL3PkBHwSaY/edit?usp=sharing
    - JAABA Setup Instructions: https://docs.google.com/document/d/1_g4UfvuIWSUyzl0OqNBMMNuLLh-bWL2n7NGrzNyp3r0/edit
## Code Breakdown

- ### DeepLabCutAutomationTemplate
    - We have created 7 Python files, that when run in order, automates the DeepLabCut component of this project. They are found in the DeepLabCutAutomation folder. The files that don't start with a number are optional and are used for diagnostic purposes. At the moment, 2_ and 3_ are not working so we suggest you use launch_deeplab_cut.sh to launch the DLC graphical user interface and complete those steps that way.

- ### JaabaScoreConversion
    - get_jaaba_predictions.py: this is a file where you can specify a JAABA experiment directory, and after running, will automatically get the predictions for behaviors specified in jab_list.txt on all the videos in the experiment directory.
    - jab_list.txt: as mentioned above, this is a file where you list the classifiers for behaviors that you want to apply to a given experiment directory.
    - score_converter.py. This is template code for extracting information from the output from JAABA. Read more about this file in the "Next Steps" section below.
- ### TrackConverter
    - dlcToExperiment.py: This is a file you use when you want to create a new JAABA experiment. You can specify the list of behaviors that you want to train classifiers for; running this file will automatically copy over the videos and .csv tracks from the DeepLabCut folder, create several copies of these videos and tracks(one for each behavior), and also populate each of those behavior folders with the CONVERTED tracks as well(tracks from DeepLabCut converted into JAABA compatible format using trackConverterCSV.py).
    - template_trx.mat: This is a file that we use during the track conversion process. Not super clear on what it contains, all we know is that it was used in the code that was given to us to convert the tracks so we're keeping it.
    - trackConverterCSV.py: This is the file that contains the function(csv_to_mat()) that actually converts DeepLabCut tracks to JAABA.
- ### Scoring
    - The scoring folder is used to run the entire workflow once the DLC and JAABA models are created and trained.
    - workflow.py is the combined workflow, running it, it will prompt you for a folder of videos to predict as well as a folder containing the .jab behavior classifiers to run.
    - dlc.py computes the position of the animal body parts in each video and outputs a CSV
    - dlc_to_jaaba.py converts the csvs to JAABA compatible experiments
    - jaaba.py applies the .jab classifiers to the experiments and outputs the results

## Workflow:
This is an outline of the workflow of this project, and it's assuming that you're starting from complete scratch. Note that if you are not starting from scratch, this is just a general order of things must be done, so you don't need to repeat every step of the process everytime you want to get prediction for JAABA, for example.

1. DeepLabCut
    1. Use [DeepLabCutAutomation/1_create_project.py](./DeepLabCutAutomation/1_create_project.py)  to create a new DLC project. 
    2. Use [DeepLabCutAutomation/launch_deeplab_cut.sh](./DeepLabCutAutomation/launch_deeplab_cut.sh) to launch the GUI to complete the following: extracting frames, labeling frames, creating training set, training). In Windows, run ```python -m deeplabcut```
    3. Use the files starting with "6" and "7" to generate pickles for all videos in the "Videos" folder and convert them from pickle to CSV.
2. JAABA
    1. Use [TrackConverter/dlcToExperiment.py](./TrackConverter/dlcToExperiment.py)  when you want to create a new JAABA experiment. This file uses the "Videos" folder we already have to make and populate a bunch of folders to satisfy the way the JAABA wants the files to be. !!! Problem Here !!!
        - Note that this is where our [TrackConverter/trackConverterCSV.py](./TrackConverter/trackConverterCSV.py) file is used.
    2. Start the JAABA GUI by opening Matlab, navigating to "Users/neurostudent/Documents/MeertsLabMachineLearning/JAABA/perframe", and typing "StartJAABA" in the Command Window.
    3. Train classifier(s): https://www.youtube.com/watch?v=6hdyVwNKepQ&t=35s
    4. Specify behaviors you want to get predictions for in [JaabaScoreConversion/jab_list.txt](./JaabaScoreConversion/jab_list.txt)
    5. Use [JaabaScoreConversion/get_jaaba_predictions.py](./JaabaScoreConversion/get_jaaba_predictions.py) to get the predictions for behaviors specified in jab_list.txt on all the videos in the experiment directory.
    6. (future) use [JaabaScoreConversion/score_converter.py](./JaabaScoreConversion/score_converter.py) to convert the JAABA predictions into a format Sarah wants(AKA the way ChamberMate produces results)
## Problems We've Encountered(and figured out): 
- In the process of converting DeepLabCut tracks into a .mat file in JAABA:
    - The dt property has to be an array of nframes-1 values where each value must be the same.
    - For multiple animals in the same video, nframes should be the same and so use the same start and endframe for each animal and use NaN if there is no value in that frame, NaN being represented as float('nan') in python.
    - [click here for the JAABA Google Groups conversation where we asked the questions for more details](https://groups.google.com/g/jaaba/c/CV6UHQ43XKg)

## Next steps:
1. Training classifiers for other behaviors other than Ins and Outs:
    - Training classifiers for these two behaviors have worked pretty well, although not perfectly. Training classifiers for the other behaviors appears to be much more difficult, as the movement pattern of the male is similar between Mounts, Intros, and Ejacs; the main difference between them seems to be a combination of timing and visual features that are not tracked(movement of body parts such as the ear). We are unsure on how to solve this problem. Given Eric Hoopfer's expertise on the topic, we would refer to him for his input on how one might tackle the problem of training classifiers for these behaviors or whether it's feasible at all.

2. As mentioned before, our classifiers for Ins and Outs work decently well. We have noticed that the reason that certain instances of the behavior are not captured is because the tracks themselves at certain times in the video are not accurate. Another way of putting it is that whenever the movement of the female rat IS being accurately tracked, JAABA does an excellent job of identifying any bouts of behavior. This makes sense, as all JAABA has to work with are the tracks that we give it(which we get from DeepLabCut). JAABA doesn't have access to anything else: the pixels on the screen for example. So, work needs to be done to try and improve the quality of the tracks we get from DeepLabCut. We believe there are several possible ways to do this:

    - Retrain DeepLabCut 
        - Conduct hyperparameter tuning. We did not try multiple sets of hyperparameters to tune the results of model; we just used standard/default values. 
        - Label more frames for DeepLabCut to use for training. We are not confident that this will make a big difference since we already have so many frames labeled.
    - Reevaluate the way we are converting from DeepLabCut tracks to JAABA-compatible .mat file(trackConverterCSV.py). This was one of the toughest parts of this project. We encountered many strange errors when trying to make sure that every field in the final .mat file matched what JAABA was expecting. It's possible that we might have made mistakes / done things in a non-optimal way during the process. 
        For example, while we track the x and y coordinates of many body parts in DeepLabCut, JAABA only takes in a single x and y coordinate for each frame. So, we have to use all of the tracked body parts from DeepLabCut to approximate the center of the animal. Currently, for each frame we basically get all of the x-coordinates of all the body parts that are tracked(AKA not a NaN value) and average them. Perhaps there is a better way to approximate the center of the animal. This is an example of something that could be revisited.
    - The quality of the videos are not great; With more HD video quality, we believe we can achieve much better results. This obviously will take a lot of work, as Sarah would have to install some new camera system and take videos of many experiments again.

3. score_converter.py. 
    - Main work here is to complete the get_results() function. This is template code(AKA this must be changed) for extracting information from the output from JAABA.

     - One of the outputs from JAABA is an array that is of length n, where n is the number of frames in the video, and each frame is either 0(behavior is not predicted to be occurring), 1(behavior is predicted to be occurring), or NaN. The template code I have right now for the get_results() function is an implementation of the following idea:

        - Start tracking a potential bout of behavior whenever we encounter a frame where it is predicted to be occurring. Once we encounter a certain number of frames in a row(variable named max_none_frames), we see how long that bout of behavior was and if it's greater than min_bout_length, then we consider that as a valid instance of the behavior and then increment the counter variable(num_bouts) and record the frame where that bout started(frame_list. Also, eventually Sarah will want all the frames in frame_list to be recorded in seconds rather than frames, which you can get by dividing the frame by the FPS(frames per second) of the video, which I believe is 60.

        - You may have a better approach to extract the information we want from the JAABA output. This is just the best way we could think of.
        
4. Investigate using custom target type. If you take a look at the "JAABA - Setup Instructions" Google doc, you'll see that there's a step called "Create custom target type for JAABA". We never implemented this step, instead choosing to use the default "flies" target type when training our classifiers. The person prior to us did create a file called "featureConfig_logan_rat.xml" that's supposed to be used for this purpose(found on the Meerts Lab google drive). We are not sure how it works and what everything inside it means. We suspect that using a custom target type might produce better results from JAABA, though we think the tracks from DeepLabCut is where our main issues lie.


