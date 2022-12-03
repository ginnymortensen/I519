#!/bin/bash

#SBATCH -J gamortenPRJ
#SBATCH -p general
#SBATCH -o filename_%j.txt
#SBATCH -e filename_%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=username@iu.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=48:00:00
#SBATCH --mem=16G

#Submit run_assembly.txt
srun bash /N/u/gamorten/Carbonate/gamortenPRJ/00-record-slurmjob.txt
