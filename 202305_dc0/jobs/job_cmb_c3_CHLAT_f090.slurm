#!/bin/bash
#SBATCH --partition=cmbas
#SBATCH --nodes=1
#SBATCH --job-name=mapsims
#SBATCH --cpus-per-task=48
#SBATCH --time=24:0:00
#SBATCH --job-name=mapsims_cmb_c3_CHLAT_f090
#SBATCH --error=logs/mapsims_cmb_c3_CHLAT_f090_%j.err
#SBATCH --output=logs/mapsims_cmb_c3_CHLAT_f090_%j.out

export OMP_NUM_THREADS=48
export NUMBA_NUM_THREADS=$OMP_NUM_THREADS

export PYTHONUNBUFFERED=1

time mapsims_run --verbose --channels='CHLAT_f090' common.toml cmb_c3.toml
