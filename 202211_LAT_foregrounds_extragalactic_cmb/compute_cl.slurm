#!/bin/bash
#SBATCH --qos=debug
#SBATCH --nodes=1
#SBATCH --time=0:30:00
#SBATCH --job-name=compute_cl
#SBATCH --error=compute_cl_%j.out
#SBATCH --output=compute_cl_%j.out

#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=272
#SBATCH --constraint=knl

export OMP_PROC_BIND=true
export OMP_PLACES=threads
export OMP_NUM_THREADS=68
export HDF5_USE_FILE_LOCKING=FALSE
export PYTHONUNBUFFERED=1

time python compute_cl.py
