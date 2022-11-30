# I519-PRJ

* This README is for github purposes only and can be deleted or written over if desired. The information in this README is identical to PRJ-README.md

Project for I519:

Clone this repository then navigate to the folder.

`cd I519-PRJ/`

Create singularity image file from .def file.

`singularity build --remote gamortenPRJ.sif SingularityPRJ.def`

Execute record file on image file to reproduce full project work.

`singularity exec -e gamortenPRJ.sif bash ./00-recordPRJ`

