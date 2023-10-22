#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>


#define SIZE 1024


int main(int argc, char ** argv){

	int myrank, nprocs, len, dest, i;
	char name[MPI_MAX_PROCESSOR_NAME];
	int *buf, *outbuf, *reduce_buf;
	MPI_Status st;
	// char *abuf;


	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
	MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
	MPI_Get_processor_name( name, &len );

	printf("Hello from processor %s[%d] %d of %d  \n", name, len, myrank, nprocs);

	if( nprocs < 2 ){
	    printf("Too small set of processors!!\n" );
	    MPI_Finalize();
	    return 1;
	}

	if( myrank == 1 ){
	    buf = (int*) malloc( sizeof(int)*(SIZE*nprocs) );
	    for( i=0; i<SIZE*nprocs; i++ )
		buf[i] = (i+1)*100+myrank;
	    for( i=0; i<nprocs; i++ )
		    printf("My[%2d]    Buf[%2d] =  %8d %8d %8d ...\n", 
    	                    myrank, i, buf[i*SIZE], buf[i*SIZE+1], buf[i*SIZE+2]);
	} 
	else {
	    buf = NULL;
	}
	
	outbuf = (int*) malloc( sizeof(int)*(SIZE) ); 
	
	MPI_Scatter(  buf, SIZE, MPI_INT,
		      outbuf, SIZE, MPI_INT, 1, MPI_COMM_WORLD );

	printf("My[%2d] outBuf = %8d %8d %8d ...\n", 
                myrank, outbuf[0], outbuf[1], outbuf[2]);

	if( myrank == 0 ){
    	    reduce_buf = (int*) malloc( sizeof(int)*(SIZE) ); 
	}
	else{
    	    reduce_buf = NULL; 
	}

	MPI_Reduce( outbuf, reduce_buf, SIZE, MPI_INT,
		    MPI_SUM, 0, MPI_COMM_WORLD );

	if( myrank == 0 ){
		printf("My[%2d] redBuf = %8d %8d %8d ...\n", 
    		        myrank, reduce_buf[0], reduce_buf[1], reduce_buf[2]);
	}

	MPI_Finalize();
	return 0;
}

