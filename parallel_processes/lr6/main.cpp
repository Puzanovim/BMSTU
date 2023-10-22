#include <mpi.h>
#include<iostream>


void print_matrix(int matrix[10][10]) {
    for(int i = 0; i != 10; ++i) {
        for(int j = 0; j != 10; ++j) {
            std::cout << matrix[i][j] << "\t";
        }
        std::cout << std::endl;
    }
}


int main(int argc, char **argv)
{
    const int SIZE = 1024;
    int rank, procs_count, len;
    char name[MPI_MAX_PROCESSOR_NAME];

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &procs_count);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Get_processor_name(name, &len);

    std::cout << "Hello from " << name << "(" << len << ") " << rank << " of " << procs_count << std::endl; 

    if (rank % 2 == 0) {
        if (rank + 1 < procs_count)
        {
            int a[10][10];
            int *b = a[0];

            for (int i = 0; i != 100; ++i)
                *(b++) = i;

            std::cout << rank << ": Sending matrix" << std::endl;
            print_matrix(a);

            MPI_Send(a, 100, MPI_INT, rank + 1, 1, MPI_COMM_WORLD);
        }
    } else {
        int a[10][10];

        MPI_Status status;
        MPI_Datatype vector, vector2;
        MPI_Aint address[2];
        MPI_Datatype type[2];

        int block_length[2];

        MPI_Type_vector(10, 1, 10, MPI_INT, &vector);

        address[0] = 0;
        address[1] = sizeof(int);

        type[0] = vector;
        type[1] = MPI_UB;

        block_length[0] = 1;
        block_length[1] = 1;

        MPI_Type_struct(2, block_length, address, type, &vector2);
        MPI_Type_commit(&vector2);
        
        MPI_Recv(a, 10, vector2, rank - 1, 1, MPI_COMM_WORLD, &status);

        MPI_Type_free(&vector);
        MPI_Type_free(&vector2);

        std::cout << rank << ": Received matrix" << std::endl;
        print_matrix(a);
    }

    MPI_Finalize();
}
