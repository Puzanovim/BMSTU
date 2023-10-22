#include <mpi.h>
#include<iostream>


int main(int argc, char **argv)
{
    const int SIZE = 1024;
    int rank, procs_count, len;
    char name[MPI_MAX_PROCESSOR_NAME];
    MPI_Status status;
    MPI_Request request;

    int *sendbuf, *recvbuf;
    sendbuf = (int *)malloc(sizeof(int) * (SIZE * 1024 + 100));
    recvbuf = (int *)malloc(sizeof(int) * (SIZE * 1024 + 100));

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &procs_count);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Get_processor_name(name, &len);

    std::cout << "Hello from " << name << "(" << len << ") " << rank << " of " << procs_count << std::endl; 

    if (rank % 2 == 0) {
        if (rank < procs_count - 1) {
            int i, j, send_size = SIZE;
            double time, data_size, bandwith;

            for (i = 0; i != SIZE * 1024; ++i) {
                sendbuf[i] = i + 10;
	        }

            for (j = 0; j != 11; ++j) {
                time = MPI_Wtime();
                for (i = 0; i != 100; ++i) {
                    MPI_Sendrecv(
                        sendbuf, send_size, MPI_INT, rank + 1, 10,
                        recvbuf, send_size + 100, MPI_INT, rank + 1, 20,
                        MPI_COMM_WORLD, &status
                    );
                }
                time = MPI_Wtime() - time;

                data_size = send_size * sizeof(int) * 200.0 / 1024;
                std::cout << rank << ": Time = " << time << " Data = " << data_size << " KByte" << std::endl;
                bandwith = data_size / (time * 1024);
                std::cout << rank << ": Bandwith[" << j << "] = " << bandwith << " MByte/sec" << std::endl;
                
                send_size *= 2;
            }
        }
        else {
	        std::cout << rank << ": Idle" << std::endl;
	    }
    }
    else {
        int i, j, send_size = SIZE;

        for (i = 0; i != 11; ++i) {
            for (j = 0; j != 100; ++j) {
                MPI_Send(sendbuf, send_size, MPI_INT, rank - 1, 20, MPI_COMM_WORLD);
                MPI_Recv(recvbuf, send_size + 100, MPI_INT, rank - 1, 10, MPI_COMM_WORLD, &status);
            }            
            send_size *= 2;
        }
    }

    MPI_Finalize();
}
