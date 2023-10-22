#include<iostream>
#include<mpi.h>


int main(int argc, char** argv) {
    int process_num, process_rank, name_len;
    char processor_name[MPI_MAX_PROCESSOR_NAME];

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &process_num);
    MPI_Comm_rank(MPI_COMM_WORLD, &process_rank);
    MPI_Get_processor_name(processor_name, &name_len);

    std::cout << "Hello world from processor " 
            << processor_name << "(" 
            << name_len << "), rank " 
            << process_rank << " of " 
            << process_num << " processors" 
            << std::endl;

    MPI_Finalize();
}
