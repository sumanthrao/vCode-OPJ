#include<stdio.h>
#include<stdlib.h>
#include"setlimits.c"
int main(int argc, char* argv[]){
	setlimits(argc,argv);
	int* arr = malloc(sizeof(int)*10000);
	// for(int i=0;i<1000000;i++){
	// 	for(int j=0;j<100000;j++){
	// 		;
	// 	}
	// }
	// Try opening more than one file 
  
   FILE *fp = NULL; 
  
   int i=0; 
  
   for (i=0; i<2; i++) 
   { 
       fp = NULL; 
       fp = fopen("test.txt","r"); 
       if(NULL == fp) 
       { 
           printf("\n fopen failed [%d]\n", i); 
           
       } 
   } 
    // Try creating a process

  if( -1 == fork())
  {
      printf("\n Creating a child process failed\n");
  }

	return 0;
}