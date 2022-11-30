# I519-PRJ

Project workflow for I519:

* Clone this repository then navigate to the folder.

`cd I519-PRJ/`

* Create singularity image file from .def file.

`singularity build --remote gamortenPRJ.sif SingularityPRJ.def`

* Execute record file on image file to reproduce full project work.

`singularity exec -e gamortenPRJ.sif bash ./00-recordPRJ`

