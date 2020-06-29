#!/bin/bash
#SBATCH --partition=debug
#SBATCH --ntasks-per-node=64 
#SBATCH --constraint=knl
#SBATCH --nodes=1
#SBATCH --time=0:30:00
#SBATCH --job-name=compute_cl
#SBATCH --error=compute_cl_%j.out
#SBATCH --output=compute_cl_%j.out

time python compute_cl.py
