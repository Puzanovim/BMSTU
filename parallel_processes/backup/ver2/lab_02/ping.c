#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define SIZE 1024

void ping_leader(int rank) {
    int *buf;
    buf = (int *) malloc(sizeof(int) * (SIZE * 1024 + 100));
    MPI_Status st;

    double time;

    for (int i = 0; i < SIZE * 1024; i++)
        buf[i] = i + 10;

    int send_size = SIZE;
    for (int iter = 0; iter < 10; iter++) {
        time = MPI_Wtime();
        for (int i = 0; i < 100; i++) {
            MPI_Send(buf, send_size, MPI_INT, rank + 1,
                     10, MPI_COMM_WORLD);
            MPI_Recv(buf, send_size + 100, MPI_INT, rank + 1,
                     20, MPI_COMM_WORLD, &st);
        }
        time = MPI_Wtime() - time;

        float sent_bytes = send_size * sizeof(int) * 100.0*2;
        float bandwith = sent_bytes / (time * 1024.0 * 1024);

        printf("[%d] Bandwith (test #%d) = %8.2f MByte/s \t dt = %6.4f  sent=%9.0f KBytes\n", rank, iter,
               bandwith,
               time, sent_bytes / 1024.0);
        send_size *= 2;

    }
    free(buf);
}

void ping_follower(int rank) {
    int *buf;
    buf = (int *) malloc(sizeof(int) * (SIZE * 1024 + 100));
    MPI_Status st;

    int send_size = SIZE;
    for (int iter = 0; iter < 10; iter++) {
        for (int i = 0; i < 100; i++) {
            MPI_Recv(buf, send_size + 100, MPI_INT, rank - 1,
                     10, MPI_COMM_WORLD, &st);
            MPI_Send(buf, send_size, MPI_INT, rank - 1,
                     20, MPI_COMM_WORLD);
        }
        send_size *= 2;
    }
    free(buf);
}

int main(int argc, char **argv) {
    int rank, nprocs, name_len;
    char name[MPI_MAX_PROCESSOR_NAME];

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Get_processor_name(name, &name_len);

    printf("Process <%s[%d]> started: rank %d of %d  \n", name, name_len, rank, nprocs);

    if (rank % 2 == 0) {
        if (rank == nprocs - 1)
            printf("[%d] Idle\n", rank);
        else
            ping_leader(rank);

    }
    else {
        ping_follower(rank);
    }
    MPI_Finalize();
    return 0;
}
