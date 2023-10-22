#include <mpi.h>
#include<iostream>
#include<string>
#include<math.h>


void print_buf(int* buf, int rank, std::string title, int i = 0, int size_row = 0) {
    std::cout << rank << ": " << title;
    for (int j = 0; j != 3; ++j) {
        std::cout << buf[i*size_row + j] << " ";
    }
    std::cout << std::endl;
}


void sumOfRow(void* buffer_in, void* buffer_out, int *len, MPI_Datatype *dptr)
{
    int *bufin = (int *)buffer_in;
    int *bufout = (int *)buffer_out;
    for (int i = 0; i != *len; ++i) {
        bufout[i] = bufin[i] + bufout[i];
    }
}


int main(int argc, char **argv)
{
    const int SIZE = 1024;
    int rank, procs_count, len, i, j;
    char name[MPI_MAX_PROCESSOR_NAME];
    std::string title;
    int *data_buffer, *reduce_buffer, *out_buffer;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &procs_count);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Get_processor_name(name, &len);

    MPI_Op op;
    MPI_Op_create(sumOfRow, 1, &op);

    std::cout << "Hello from " << name << "(" << len << ") " << rank << " of " << procs_count << std::endl; 

    if (rank == 0) {
        data_buffer = (int*) malloc(sizeof(int) * SIZE * procs_count);
        reduce_buffer = (int*) malloc(sizeof(int) * SIZE);
        out_buffer = (int*) malloc(sizeof(int) * SIZE);

        for (i = 0; i != (SIZE * procs_count); ++i) {
            data_buffer[i] = i;
        }
        for (i = 0; i < procs_count; ++i) {
            title = "Buffer №" + std::to_string(i) + " = ";
            print_buf(data_buffer, rank, title, i, SIZE);
        }

        MPI_Scatter(data_buffer, SIZE, MPI_INT, out_buffer, SIZE, MPI_INT, 0, MPI_COMM_WORLD);

        title = "Out buffer = ";
        print_buf(out_buffer, rank, title);
        
        MPI_Reduce(out_buffer, reduce_buffer, SIZE, MPI_INT, op, 0, MPI_COMM_WORLD);

        title = "Reduced = ";
        print_buf(reduce_buffer, rank, title);
    } else {
        data_buffer = NULL;
        reduce_buffer = NULL;
        out_buffer = (int*) malloc(sizeof(int) * SIZE);

        MPI_Scatter(data_buffer, SIZE, MPI_INT, out_buffer, SIZE, MPI_INT, 0, MPI_COMM_WORLD);
        
        title = "Out buffer = ";
        print_buf(out_buffer, rank, title);

        MPI_Reduce(out_buffer, reduce_buffer, SIZE, MPI_INT, op, 0, MPI_COMM_WORLD);
    }

    MPI_Finalize();
}

