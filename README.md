## I519-PRJ
Project for I519

Create singularity image file from .def file with 
`singularity build --remote gamortenPRJ.sif SingularityPRJ.def`
Execute record file on image file to reproduce full project work
`singularity exec -e gamortenPRJ.sif bash ./00-recordPRJ`

