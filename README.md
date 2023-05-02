# MeertsLabMachineLearning

## Introduction
This is project is trying to use DeepLabCut and JAABA to classify animal behavior. The idea is that we use DeepLabCut as a non-invasive multi-part tracker to get the tracks of the animals and then we feed those tracks into JAABA to train behavior classifiers that will then be able to predict bouts of animal behavior on new videos.

## Getting Ready
We recommend installing [VS Code](https://code.visualstudio.com/download) and [git](https://git-scm.com/download) in order to clone the code and run it locally.

You will need [Anaconda](https://www.anaconda.com/download/) to run DeepLabCut

With the code downloaded and Anaconda installed, you will then have to open up the terminal and navigate to [DeepLabCut/conda-environments](./DeepLabCut/conda-environments) folder. If you open this project in VS Code and open a terminal you simply need to run the following commands.


<!--
Is not working at the moment
git submodule update --init             # download the DeepLabCut code
cd DeepLabCut/conda-environments        # navigate to the correct folder
conda env create -f DEEPLABCUT.yaml     # install the DeepLabCut Anaconda environment (dependencies)
-->
```console
conda create -n DEEPLABCUT python=3.10
conda activate DEEPLABCUT
conda install -y -q python-dotenv
pip install "deeplabcut[tf,gui]"
conda deactivate
```

In the [rat-behavior-classifier folder](.), you must create a folder named Videos within which you place the video (.mp4) of each experiment you will be using to train the model.

Before you begin you will need to open [DeepLabCutAutomation/1_create_project.pyw](./DeepLabCutAutomation/1_create_project.pyw) an adjust the ```PROJECT_NAME```, ```YOUR_NAME``` and ```edits``` to your specific project requirements.

## Running the Code


## Code Breakdown
### TrackConverterTemplate
The trackConverter is the code that we are using to convert the output from DeepLabCut (csv) into a valid input (trx files) for JAABA.

### DeepLabCutAutomationTemplate
This folder is a template for creating and running a MacOS DeepLabCut project. It contains:
1. create_project.pyw: Code to create a new project, customize the config file and extract some preliminary frames for labeling
2. extract_frames.pyw: Code to launch DLC's GUI for manualy extracting specified frames for labeling
3. label_frames.pyw: Code to launch DLC's GUI for labeling extracted frames
4. create_training_set.py: Code to convert all frames into a training and testing dataset. This should be only run after labeling all frames as it will treat unlabeled frames as having no target in them, but still include them in the dataset.
5. train.pyw: Code to start the training process after the training and testing dataset is created.

## Problems We've Encountered So Far: 
- In the process of converting DeepLabCut tracks into a .mat file in JAABA:
    - The dt property is an array of nframes-1 values where each value must be the same.
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
    - The quality of the videos are not great. With more HD video quality, we believe we can achieve much better results. This obviously will take a lot of work, as Sarah would have to install some new camera system and take videos of many experiments again.

3. score_converter.py. 
    - Main work here is to complete the get_results() function. This is template code for extracting information from the output from JAABA(AKA this should be definitely be changed).

     - One of the outputs from JAABA is an array that is of length n, where n is the number of frames in the video, and each frame is either 0(behavior is not predicted to be occurring), 1(behavior is predicted to be occurring), or NaN. The template code I have right now for the get_results() function is an implementation of the following idea:

    - Start tracking a potential bout of behavior whenever we encounter a frame where it is predicted to be occurring. Once we encounter a certain number of frames in a row(variable named max_none_frames), we see how long that bout of behavior was and if it's greater than min_bout_length, then we consider that as a valid instance of the behavior and then increment the counter variable(num_bouts) and record the frame where that bout started(frame_list. Also, eventually Sarah will want all the frames in frame_list to be recorded in seconds rather than frames, which you can get by dividing the frame by the FPS(frames per second) of the video, which I believe is 60.

    - You may have a better approach to extract the information we want from the JAABA output. This is just the best way we could think of.


