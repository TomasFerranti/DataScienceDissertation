# SMTools: A Data Pipeline for 3D Visual Interpretation of Images

Created in partnership with _imagineRio_ for the project _Vistas Situadas do Rio de Janeiro_ of _Instituto Moreira Salles (IMS)_, _SMTools_ is an aggregated work of over two years organized and explained in a dissertation as requirement for the undergraduate degree in Data Science and Artificial Intelligence at _EMAp FGV-RJ_. It is a continuation of my previous work for the undergraduate degree in Applied Mathematics also at _EMAp FGV-RJ_.

Historic photographic collections are valuable documents of urban evolution through time. Many historic buildings in such collections may have been demolished or changed over time. Digital modeling of such buildings is challenging due to the reduced amount of information available that might be limited to a few images and schematic drawings. 

This work presents a method to create a 3D set of connected rectangles that approximates elements of a scene (such as walls, floors, and roofs) from a single image. We adopt a pinhole camera model to recover the image perspective and extract the geometry and texture of planes parallel to world axes. Besides the image, other inputs are points and segments annotation provided by the user, further optimized using an automatic adjustment. 

Knowing the exact dimension of an object within the model allows the retrieval of its real scale. For images which are from stereo cameras, if the stereo pair is available we can also automatically split the pair and calibrate one from the others calibration through stereo propagation. Results show that, from a single image, our method creates a good visualization of the scene. In additional, the constructed pipeline merges each technique fluidly creating a final software of practical application.

This pipeline was developed to be one of the approaches for 3D visualization on the searchable digital atlas [imagineRio](https://www.imaginerio.org/), which illustrates the social and urban evolution of Rio de Janeiro. Below follows how this repository is organized and a tutorial on how to use.

# Files organization

The files of the project are separated into the following folders:

- `docs/`: files of documenting papers and manuals of use;

- `presentations/`: files for the presentations of the project;

- `figs/`: figures used in documents or presentations;

- `src/TextureExtractor`: tool with dockerized source code of Node web application with Javascript;

- `src/SMTools`: tool with dockerized source code of scripts terminal interface with Python;
  
- `images/`: folders to look for images when running;

- `calib/`: folders to look for images calibrations when running;

# Requirements

It is necessary to have a [Docker](https://www.docker.com/) and [Docker-Compose](https://docs.docker.com/compose/) installation. Currently it has three bash scripts which are used to build, run and clear the files needed for the project. These were created with Linux commands and environment (if you use other operational system you are encouraged to find equivalent commands and make a pull request).

# How to run

Currently you can only run both tools at the same time. For that you can start a terminal inside the root folder and run the following commands one at a time

> sudo bash build.sh
> 
> sudo bash run.sh
>
> sudo bash clear.sh

where _build.sh_ creates all docker images, folders and files needed, _run.sh_ starts the server and launches the interface and _clear.sh_ clears everything we builded. If you have any ideas or suggestions for improvement please file an issue in this repository.