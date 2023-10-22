#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define SIZE 1024

int main(int argc, char **argv)
{
	int myrank, nprocs, len;
	char name[MPI_MAX_PROCESSOR_NAME];
	int *buf_in, *buf_out;

	MPI_Status st;
	MPI_Request re;
	double times[10];
	double data[10];

	buf_in = (int *)malloc(sizeof(int) * (SIZE * 1024 + 100));
	buf_out = (int *)malloc(sizeof(int) * (SIZE * 1024 + 100));

	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
	MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
	MPI_Get_processor_name(name, &len);

	printf("Hello from processor %s[%d] %d of %d  \n", name, len, myrank, nprocs);

	for (int i = 0; i < SIZE * 1024; i++)
		buf_out[i] = i + 10 * myrank;

	if (myrank % 2 == 0)
	{
		if (myrank < nprocs - 1)
		{
			int i, cl, sz = SIZE;
			double time;

			for (cl = 0; cl < 11; cl++)
			{

				time = MPI_Wtime();
				for (i = 0; i < 100; i++)
				{
					MPI_Isend(buf_out, sz, MPI_INT, myrank + 1,
							  10, MPI_COMM_WORLD, &re);

					// if MPI_Wait -> deadlock

					MPI_Recv(buf_in, sz + 100, MPI_INT, myrank + 1,
							 20, MPI_COMM_WORLD, &st);
					MPI_Wait(&re, &st);
				}
				time = MPI_Wtime() - time;
				printf("[%d] Time = %lf  Data=%9.0f KByte\n",
					   myrank,
					   time,
					   sz * sizeof(int) * 200.0 / 1024);
				printf("[%d]  Bandwith[%d] = %lf MByte/sek  cl=%d\n",
					   myrank,
					   cl,
					   sz * sizeof(int) * 200 / (time * 1024 * 1024),
					   cl);
				times[cl] = time;
				data[cl] = ((double)sz) * sizeof(int) * 200.0 / (1024.0 * 1024.0);

				printf("\t[%d]  Sent: ", myrank);
				for (int i = 0; i < 10; i++)
					printf("%4d ", buf_out[i]);
				printf("\n\t[%d] Received: ", myrank);
				for (int i = 0; i < 10; i++)
					printf("%4d ", buf_in[i]);
				printf("\n");

				sz *= 2;
			}
		}
		else
			printf("[%d] Idle\n", myrank);
	}
	else
	{
		int i, cl, sz = SIZE;
		for (cl = 0; cl < 11; cl++)
		{

			for (i = 0; i < 100; i++)
			{
				MPI_Issend(buf_out, sz, MPI_INT, myrank - 1,
                                           20, MPI_COMM_WORLD, &re);
				MPI_Recv(buf_in, sz + 100, MPI_INT, myrank - 1,
						 10, MPI_COMM_WORLD, &st);
			}

			printf("\t[%d]  Sent: ", myrank);
			for (int i = 0; i < 10; i++)
				printf("%4d ", buf_out[i]);
			printf("\n\t[%d] Received: ", myrank);
			for (int i = 0; i < 10; i++)
				printf("%4d ", buf_in[i]);
			printf("\n");

			sz *= 2;
		}
	}

	MPI_Finalize();
	return 0;
}
