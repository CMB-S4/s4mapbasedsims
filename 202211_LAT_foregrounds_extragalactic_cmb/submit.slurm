#!/bin/bash
#SBATCH --qos=regular
#SBATCH --ntasks-per-node=1
#SBATCH --constraint=knl
#SBATCH --nodes=1
#SBATCH --time={hours}:{minutes}:00
#SBATCH --job-name=mapsims_{simulation_type}_{nside}_{channels}
#SBATCH --error=log_lsq/mapsims_{simulation_type}_{nside}_{channels}_%j.err
#SBATCH --output=log_lsq/mapsims_{simulation_type}_{nside}_{channels}_%j.out
#SBATCH --cpus-per-task=272

export OMP_PROC_BIND=true
export OMP_PLACES=threads
export OMP_NUM_THREADS=68
export NUMBA_NUM_THREADS=$OMP_NUM_THREADS

export PYTHONUNBUFFERED=1

module load python
conda activate pycmbprod

time mapsims_run --nside={nside} --verbose --channels='{run_channels}' common.toml {config_file}.toml
