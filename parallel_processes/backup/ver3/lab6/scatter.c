#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define SIZE 1024
#define MODULE 997

void modSum(int* in, int* inout, int *len, MPI_Datatype *dptr)
{
    for (int i=0; i< *len; ++i) {
        inout[i] = (in[i] + inout[i]) % MODULE;
    }
}

void ping_leader(int rank, int nprocs) {
    int *data, *part, *reduce;
    MPI_Status st;

    data = (int*) malloc( sizeof(int)*(SIZE*nprocs) );
    reduce = (int*) malloc( sizeof(int)*(SIZE) );
    part = (int*) malloc( sizeof(int)*(SIZE) );

    for(int i=0; i<SIZE*nprocs; i++ )
        data[i] = i;

    for(int i=0; i<nprocs; i++)
        printf("[%2d] Leader buffer, part[%2d]:  %8d %8d %8d ...\n",
               rank, i, data[i*SIZE], data[i*SIZE+1], data[i*SIZE+2]);


    MPI_Op mod_sum_op;
    MPI_Op_create(modSum, 1, &mod_sum_op);
    MPI_Scatter( data, SIZE, MPI_INT,
                  part, SIZE, MPI_INT, 0, MPI_COMM_WORLD );

    printf("[%2d] Received part = %8d %8d %8d ...\n",
           rank, part[0], part[1], part[2]);

    MPI_Reduce( part, reduce, SIZE, MPI_INT,
                mod_sum_op, 0, MPI_COMM_WORLD );

    printf("[%2d] Reduced = %d %8d %8d ...\n",
           rank, reduce[0], reduce[1], reduce[2]);

    int result = 0;
    for(int i=0; i<SIZE; i++ )
        result = (result + reduce[i]) % MODULE;
    printf("[%2d] Leader sum (mod %d) result = %8d\n",
           rank, MODULE, result);



    free(part);
    free(reduce);
    free(data); // todo?
}

void ping_follower(int rank) {
    int *data, *part, *reduce;
    MPI_Status st;

    data = NULL;
    reduce = NULL;
    part = (int*) malloc( sizeof(int)*(SIZE) );
    MPI_Scatter(  data, SIZE, MPI_INT,
                  part, SIZE, MPI_INT, 0, MPI_COMM_WORLD );

    printf("[%2d] Received part = %8d %8d %8d ...\n",
           rank, part[0], part[1], part[2]);

    MPI_Reduce( part, reduce, SIZE, MPI_INT,
                MPI_SUM, 0, MPI_COMM_WORLD );


    free(part);

}

int main(int argc, char **argv) {
    int rank, nprocs, name_len;
    char name[MPI_MAX_PROCESSOR_NAME];

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Get_processor_name(name, &name_len);

    printf("Process <%s[%d]> started: rank %d of %d  \n", name, name_len, rank, nprocs);

    if (rank == 0) {
        ping_leader(rank, nprocs);
    }
    else {
        ping_follower(rank);
    }
    MPI_Finalize();
    return 0;
}