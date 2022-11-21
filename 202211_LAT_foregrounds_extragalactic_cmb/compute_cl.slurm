#!/bin/bash
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --time=3:30:00
#SBATCH --job-name=compute_cl
#SBATCH --error=compute_cl_%j.out
#SBATCH --output=compute_cl_%j.out

#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=272
#SBATCH --constraint=knl

export OMP_PROC_BIND=true
export OMP_PLACES=threads
export OMP_NUM_THREADS=68
export HDF5_USE_FILE_LOCKING=FALSE
export PYTHONUNBUFFERED=1

module load python
conda activate pycmbprod

time python compute_cl.py
