#include "Mille.h"
#include <iostream>

using namespace std;

int main(int argc, char *argv[] ){
   cout << "argc " << argc << endl;
   std::cout << " Start " << std::endl;

   Mille* mille = new Mille("test.out", true, false);
   delete mille;


   return 0;



}
