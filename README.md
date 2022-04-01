# MeertsLabMachineLearning

## Introduction
This is project is trying to use DeepLabCut and JAABA to classyify animal behavior. The idea is that we use DeepLabCut as a non-invasive multi-part tracker that we then feed into JAABA to create behavior classifiers in order to facilitate the identification of animal behaviors.

## TrackConverterTemplate
The trackConverter is the code that we are using to convert the output from DeepLabCut (csv) into a valid input (trx files) for JAABA.

## DeepLabCutAutomationTemplate
This folder is a template for creating and running a MacOS DeepLabCut project. It contains:
1. create_project.pyw: Code to create a new project, customize the config file and extract some preliminary frames for labeling
2. extract_frames.pyw: Code to launch DLC's GUI for manualy extracting specified frames for labeling
3. label_frames.pyw: Code to launch DLC's GUI for labeling extracted frames
4. create_training_set.py: Code to convert all frames into a training and testing dataset. This should be only run after labeling all frames as it will treat unlabeled frames as having no target in them, but still include them in the dataset.
5. train.pyw: Code to start the training process after the training and testing dataset is created.

## Todo:
- Create files to automate process of analyze videos(AKA produce h5 file)
- Update conversion code to read in h5 file.
- Look into why the video fps is low in JAABA

## Problems We've Encountered So Far: 
- The JAABA software is expecting numbers represented in a certain way using a specific amount of bytes and so all numbers must be of float type in python.
- The dt property is an array of nframes-1 values where each value must be the same.
- For multiple animals in the same video, nframes should be the same and so use the same start and endframe for each animal and use NaN if there is no value in that frame, NaN being represented as float('nan') in python.
- [click here for the JAABA Google Groups conversation where we asked the questions for more details](https://groups.google.com/g/jaaba/c/CV6UHQ43XKg)
