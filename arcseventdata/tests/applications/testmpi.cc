#include "mpi.h"
#include <stdio.h>

int main(int argc, char *argv[]) 
{
  int  numtasks, rank, rc; 

  rc = MPI_Init(&argc,&argv);
  if (rc != MPI_SUCCESS) {
    printf ("Error starting MPI program. Terminating.\n");
    MPI_Abort(MPI_COMM_WORLD, rc);
  }

  MPI_Comm_size(MPI_COMM_WORLD,&numtasks);
  MPI_Comm_rank(MPI_COMM_WORLD,&rank);
  printf ("Number of tasks= %d My rank= %d\n", numtasks,rank);

  double *p = new double[10];
  printf( "allocated poitner: %p\n", p );
  if  (rank == 0) p[0] = 999;
  printf( "p[0] =  %g\n", p[0] );
  delete [] p;

  MPI_Finalize();
}
