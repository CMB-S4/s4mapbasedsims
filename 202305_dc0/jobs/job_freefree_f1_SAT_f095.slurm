#!/bin/bash
#SBATCH --partition=cmbas
#SBATCH --nodes=1
#SBATCH --job-name=mapsims
#SBATCH --cpus-per-task=48
#SBATCH --time=24:0:00
#SBATCH --job-name=mapsims_freefree_f1_SAT_f095
#SBATCH --error=logs/mapsims_freefree_f1_SAT_f095_%j.err
#SBATCH --output=logs/mapsims_freefree_f1_SAT_f095_%j.out

export OMP_NUM_THREADS=48
export NUMBA_NUM_THREADS=$OMP_NUM_THREADS

export PYTHONUNBUFFERED=1

time mapsims_run --verbose --channels='SAT_f095' common.toml freefree_f1.toml
