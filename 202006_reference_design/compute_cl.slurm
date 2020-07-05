#!/bin/bash
#SBATCH --partition=regular
#SBATCH --ntasks-per-node=64 
#SBATCH --constraint=knl
#SBATCH --nodes=1
#SBATCH --time=3:00:00
#SBATCH --job-name=compute_cl
#SBATCH --error=compute_cl_%j.out
#SBATCH --output=compute_cl_%j.out

export HDF5_USE_FILE_LOCKING=FALSE
time python compute_cl.py LAT
