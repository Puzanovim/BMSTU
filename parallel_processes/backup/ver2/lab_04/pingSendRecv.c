#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define SIZE 1024
// #define SIZE 128

int main(int argc, char **argv)
{
	int myrank, nprocs, len;
	char name[MPI_MAX_PROCESSOR_NAME];
	int *buf;
	MPI_Status st;

	buf = (int *)malloc(sizeof(int) * (SIZE * 1024 + 100));
	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
	MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
	MPI_Get_processor_name(name, &len);

	printf("Hello from processor %s[%d] %d of %d  \n", name, len, myrank, nprocs);

	if (myrank % 2 == 0)
	{
		if (myrank < nprocs - 1)
		{

			int i, cl, sz = SIZE;
			double time;

			for (i = 0; i < SIZE * 1024; i++)
				buf[i] = i + 10;

			for (cl = 0; cl < 11; cl++)
			{
				time = MPI_Wtime();
				for (i = 0; i < 100; i++)
				{
					MPI_Send(buf, sz, MPI_INT, myrank + 1,
							 10, MPI_COMM_WORLD);
					//		      printf( "[%d]* ", myrank );
					MPI_Recv(buf, sz + 100, MPI_INT, myrank + 1,
							 20, MPI_COMM_WORLD, &st);
				}
				printf("\n");
				time = MPI_Wtime() - time;
				printf("[%d] Time = %lf  Data=%9.0f KByte\n",
					   myrank,
					   time,
					   sz * sizeof(int) * 200.0 / 1024);
				printf("[%d]  Bandwith[%d] = %lf MByte/sek\n",
					   myrank,
					   cl,
					   sz * sizeof(int) * 200 / (time * 1024 * 1024));
				sz *= 2;

				printf("[%d] ", myrank);
				for (i = 0; i < 10; i++)
					printf("%5d", buf[i]);
				printf("\n");
			}
		}
		else
			printf("[%d] Idle\n", myrank);
	}
	else
	{
		int i, cl, sz = SIZE;
		int *bufI, *tmp;
		bufI = (int *)malloc(sizeof(int) * (SIZE * 1024 + 100));

		for (i = 0; i < SIZE * 1024; i++)
			buf[i] = i + 100;

		for (cl = 0; cl < 11; cl++)
		{

			for (i = 0; i < 100; i++)
			{
				MPI_Sendrecv(buf, sz, MPI_INT, myrank - 1, 20,
							 bufI, sz + 100, MPI_INT, myrank - 1, 10,
							 MPI_COMM_WORLD, &st);
				tmp = buf;
				buf = bufI;
				bufI = tmp;
			}
			sz *= 2;

			printf("[%d] ", myrank);
			for (i = 0; i < 10; i++)
				printf("%5d", buf[i]);
			printf("\n");
		}
	}
	MPI_Finalize();
	free(buf);
	return 0;
}
