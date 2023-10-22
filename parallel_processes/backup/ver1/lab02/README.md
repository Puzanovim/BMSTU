mpicc ping.c -o p

ls -l

./p

mpirun -np 2 p | more

Для параллельки job.sh

sinfo

squeue

sbatch job.sh

ls && cat slurm
