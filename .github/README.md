# gamortenPRJ - submission for I519 Fall 2022 Project

Project workflow for I519:

* Clone this repository then navigate to the folder.

`cd gamortenPRJ/`

* Load singularity module then create singularity image file from .def file.

`singularity build --remote gamortenPRJ.sif SingularityPRJ.def`

* Execute record file on image file to reproduce full project work (15-20 minutes to complete).

`singularity exec -e gamortenPRJ.sif bash ./00-recordPRJ`

