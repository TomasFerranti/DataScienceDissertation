# SMTools

Repository created to store the code made for the project Vistas Situadas do Rio de Janeiro in FGV-RJ, with collaboration between Rice University, ImagineRio and Instituto Moreira Salles.

## Installing the requirements

The main file of this project is "interface.py" on the root folder, where we have multiple options of Stereo Matching Tools available to employ on target stereo images. With the installation of "Python 3.8.10" and the package manager "pip", one can easily install the requirements for all the scripts with

    pip install -r requirements.txt

while on the root folder. 

Another step before doing anything is cloning and installing the requirements of our other project called TextureExtractor, available at https://github.com/TomasFerranti/TextureExtractor, under the root folder. After that, we just need to run the script with

    python3 interface.py

and voilà.

## How does it work?

Currently there is a Bachelor Dissertation in the works to explain all the tool functionalities more detailed. A current fluxogram can be visualized in the figure below:

![alt text](fluxogram.png "Fluxogram of Stereo Images")

The file "interface.py" has the option to run any .py script on a image/calibration separately, while it also has an option to run through the entire pipeline with a stereo image. There is an additional script "shared_functions.py" which has all common functions used throughout the process.