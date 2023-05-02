# DeepLabCut
## Setup Instructions

1. ### Download and Install Anaconda
    * Go to this link: https://www.anaconda.com/distribution/ 
    * Scroll down almost to the bottom and under Anaconda Installers select Graphical Installer for your operating system
    * Open the installer and click through it
    * To check that Anaconda is installed run this line in the command line(terminal on mac): conda list

2. ### Download DeepLabCuts
    * Open the command line(terminal on mac) and navigate to the folder you want put DeepLabCuts
    * To navigate in the command line you can use the following commands:
        * To list the items in the current location: ls
        * To move to a folder: cd FolderName
        * To move up to the parent folder: cd ..
        * To get the location right, you can drag the folder and drop it into Terminal. Alternatively, you can (on Windows) hold SHIFT and right-click > Copy as path, or (on Mac) right-click and while in the menu press the OPTION key to reveal Copy as Pathname.
    * Download by running: git clone https://github.com/AlexEMG/DeepLabCut.git
3. ### Create the conda environment
    * Now navigate to the conda-environment folder
        * If you do this directly after the previous step you can just run this command: cd DeepLabCut/conda-environments
    * Create the conda environment by running the following command: conda env create -f DEEPLABCUT.yaml
    * Activate the environment: conda activate DEEPLABCUT
4. ### Open DeepLabCuts
    * Navigate to the DeepLabCut folder
        * If you do this directly after the previous step you can just run this command: cd ..
    * Run the following commands:
        * conda install python.app
        * To open Python run: pythonw (or ipython in Windows)
        * The command line should have >>> before each line now
        * Now run: import deeplabcut
        * To open the GUI run: deeplabcut.launch_dlc()
5. ### Using DeepLabCut
    * We have created 7 Python files, that when run in order, automates the DeepLabCut component of this project. They are found in the DeepLabCutAutomation folder. The files that don't start with a number are optional and are used for diagnostic purposes.
        1. Create the project
            * Specify the Project name and the Experimenter name
            * You can also change the bodyparts and the skeleton(how the bodyparts are connected)
            * Run the file
        2. Extract frames
            * A number of frames are already automatically extracted from running the previous step, but in order to get optimal results, we want to select some "special" frames to make sure the network can recognize the animals in a variety of different places. For instance, when the two rats are interacting. Running the file will launch a GUI to do this.
        3. Label frames
            * Run this function to label extracted frames. You will want to select a folder under the labeled-data folder which contains sub directories for each video with the extracted frames. Select one video subdirectory, go through and label it (there is a help option in the GUI) and then click save. You can save and quit at any point. Once you press quit it will ask if you want to label another video. Repeat until you are done. You can always quit and run this function another time to continue where you left off as long as you have saved your work.
        4. Create training set
            * Run this function to split up the labeled frames into a training and testing dataset.
        5. Train 
            * Run this function to begin the training on the dataset. This usually takes a few days.
        6. Generate pickle file
            * After training has finished, run this function to generate the h5 file containing predictions.
        7. Convert pickle to CSV
            * Run this function to convert the generated h5 files to csv's so we can work with them.
            * Now time for JAABA!


