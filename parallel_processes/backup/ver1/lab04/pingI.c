#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>


#define SIZE 1024

void approximation( int rank, int n, double *x, double *y, double *a, double *b );


int main(int argc, char ** argv){

	int myrank, nprocs, len;
	char name[MPI_MAX_PROCESSOR_NAME];
	int *buf, *bufI;
	MPI_Status st;
	MPI_Request re;
	double times[10];
	double data[10]; 

	buf = (int*) malloc( sizeof(int)*(SIZE*1024 + 100) );
	bufI = (int*) malloc( sizeof(int)*(SIZE*1024 + 100) );
	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
	MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
	MPI_Get_processor_name( name, &len );

	printf("Hello from processor %s[%d] %d of %d  \n", name, len, myrank, nprocs);

	if ( myrank % 2 == 0  ){
	    if( myrank < nprocs-1 ){
	   	int i, cl,sz=SIZE;
		double time;

 		for( i=0; i<SIZE*1024; i++ )
		    buf[i] = i+10;

		for( cl=0; cl<11; cl++ ){

		   time = MPI_Wtime();
		   for( i= 0; i<100; i++ ){
		      MPI_Issend( buf, sz, MPI_INT, myrank+1, 
					10, MPI_COMM_WORLD, &re );
		      // MPI_Wait( &re, &st );   // Deadlock!!!!!

		      MPI_Recv( bufI, sz+100, MPI_INT, myrank+1,
					20, MPI_COMM_WORLD, &st );
		      MPI_Wait( &re, &st );  // Succes!!!!
		    }
         	    time = MPI_Wtime() - time;
		    printf( "[%d] Time = %lf  Data=%9.0f KByte\n", 
                            myrank, 
                            time, 
                            sz*sizeof(int)*200.0/1024 );
		    printf( "[%d]  Bandwith[%d] = %lf MByte/sek  cl=%d\n", 
			 myrank,
			 cl,  
                         sz*sizeof(int)*200/(time *1024*1024),
			 cl );
		    times[cl] = time;
		    data[cl] = ((double) sz)*sizeof(int)*200.0/(1024.0*1024.0);
		    sz *=2;
		}

/*
		double band, lattence;

		approximation( myrank, 10, data, times, &band, &lattence );
//		printf( "[%d] Bandwith =%lfMByte/sek    Lattence = %lf mksec\n", 
  		printf( "[%d] Bandwith =%lf    Lattence = %lf \n", 
            	        myrank, band, //  /(1024*1024),  
                	lattence  ); // /(100 *1000000 ) );
*/    

	    } else
		printf("[%d] Idle\n", myrank );
	}
	else {
		int i,cl,sz=SIZE;
		for( cl=0; cl<11; cl++){

		    for( i=0; i<100; i++){
			MPI_Issend( buf, sz, MPI_INT, myrank-1,
					20, MPI_COMM_WORLD, &re );
			MPI_Recv( bufI, sz+100, MPI_INT, myrank-1,
					10, MPI_COMM_WORLD, &st );
			MPI_Wait( &re, &st );
		    }
		    sz *=2;
		}


	}



	MPI_Finalize();
	return 0;

}

