#!/bin/bash
#SBATCH --partition=soap
#SBATCH --ntasks-per-node=48
#SBATCH --nodes=1
#SBATCH --time={hours}:{minutes}:00
#SBATCH --job-name=mapsims_{simulation_type}_{nside}_{channels}
#SBATCH --error=mapsims_{simulation_type}_{nside}_{channels}_%j.err
#SBATCH --output=mapsims_{simulation_type}_{nside}_{channels}_%j.out

time mapsims_run --nside={nside} --channels='{run_channels}' common.toml {config_file}.toml
