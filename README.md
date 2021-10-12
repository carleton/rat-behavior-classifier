# MeertsLabMachineLearning
## Introduction
This is project is trying to use DeepLabCut and JAABA to classyify animal behavior. The idea is that we use DeepLabCut as a non-invasive multi-part tracker that we then feed into JAABA to create behavior classifiers in order to facilitate the identification of animal behaviors.

## TrackConverter
The trackConverter is the code that we are using to convert the output from DeepLabCut (csv) into a valid input (trx files) for JAABA.
### Problems We've Encounter So Far:
- The JAABA software is expecting numbers represented in a certain way using a specific amount of bytes and so all numbers must be of float type in python.
- The dt property is an array of nframes-1 values where each value must be the same.
- For multiple animals in the same video, nframes should be the same and so use the same start and endframe for each animal and use NaN if there is no value in that frame, NaN being represented as float('nan') in python.
