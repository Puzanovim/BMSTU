#!/bin/bash
#SBATCH --job-name="lab1"
#SBATCH --partition=debug
#SBATCH --nodes=10
#SBATCH --time=0-00:05:00
#SBATCH --ntasks-per-node=1
#SBATCH --mem=1992

mpirun -np 10 a.out
