#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define SIZE 1024

void ping_leader(int rank, int nprocs) {
    int  a[10][10];

    int i,j, *b;
    b = a[0];

    for( i=0; i<100; i++ )
        *(b++) = i;

    printf("[%d] Sending matrix\n", rank );
    for( i=0; i<10; i++ ){
        for( j=0; j<10; j++ )
            printf( "%6d", a[i][j] );
        printf( "\n" );
    }

    MPI_Send( a, 100, MPI_INT,  rank+1, 1, MPI_COMM_WORLD );
}

void ping_follower(int rank) {
    int  a[10][10];
    MPI_Status st;

    MPI_Datatype vector;
    MPI_Type_vector( 10, 1, 10, MPI_INT, &vector );    // count, block-length, stride


    MPI_Datatype sparse_vector;
    MPI_Aint addresses[2];
    MPI_Datatype types[2];
    int blocklens[2];         // number of elements in block

    types[0] = vector;
    types[1] = MPI_UB;     // upper bound
    blocklens[0] = 1;
    blocklens[1] = 1;
    addresses[0] = 0;
    addresses[1] = sizeof(int);  // set upperbound (offset between stucts) to 1 element, vector'll jump out of it gathering info
    MPI_Type_struct( 2, blocklens, addresses, types, &sparse_vector );   // count, blocklens, indices, types
    MPI_Type_commit( &sparse_vector );

    MPI_Recv( a, 10, sparse_vector, rank-1, 1, MPI_COMM_WORLD, &st );

    MPI_Type_free( &vector );
    MPI_Type_free( &sparse_vector );

    printf("[%d] Received transposed matrix\n", rank);
    int i,j;
    for( i=0; i<10; i++ ){
        for( j=0; j<10; j++ )
            printf( "%6d", a[i][j] );
        printf( "\n" );
    }
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
    else if (rank == 1){
        ping_follower(rank);
    }
    else{
        printf("[%d] Ignoring process\n", rank);
    }
    MPI_Finalize();
    return 0;
}



