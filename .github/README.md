# gamortenPRJ - submission for I519 Fall 2022 Project

Project workflow for I519:

* Clone this repository then navigate to the folder.
`git clone https://github.com/ginnymortensen/gamortenPRJ`
`cd gamortenPRJ`

* Load singularity module then pull project image.
`module load singularity`
`singularity pull --arch amd64 library://gamorten/prj/gamorten-prj.sif:i519-fall`

* Execute record file on image file to reproduce full project work (15-20 minutes to complete).
`singularity exec -e gamorten-prj.sif_i519-fall.sif bash ./00-recordPRJ`

*This README file is hidden such as to not interfere with data acquisition step of record execution*

