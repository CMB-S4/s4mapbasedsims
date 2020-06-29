#!/bin/bash
#SBATCH --partition=soap
#SBATCH --ntasks-per-node=48 
#SBATCH --nodes=1
#SBATCH --time=4:00:00
#SBATCH --job-name=compute_cl
#SBATCH --error=compute_cl_%j.out
#SBATCH --output=compute_cl_%j.out

time python compute_cl.py
