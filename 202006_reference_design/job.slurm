#!/bin/bash
#SBATCH --qos=regular
#SBATCH --time=5:30:00
#SBATCH --nodes=1
#SBATCH --tasks-per-node=64
#SBATCH --constraint=knl

export HDF5_USE_FILE_LOCKING=FALSE
bash run.sh s4_reference_design_noise_atmo_7splits.toml
