#include "MilleParser.h"

#include "TApplication.h"

#include <iostream>
#include <string>
#include <cstdlib>
#include <sstream>

using namespace std;

int main(int argc, char *argv[] ){
   cout << "argc " << argc << endl;
   if(argc < 2) {
      cout << " --------------------------------------------- " << endl;
      cout << " printMille:  " << endl;
      cout << " --------------------------------------------- " << endl;
      cout << "  -> you need to specify 1 parameters " << endl;
      cout << "   input file   " << endl;
      cout << "   outfile name (Optional)   " << endl;
      cout << "   \"top\" or \"bottom\" (Optional)" << endl;
      cout << "   max trks (Optional)   " << endl;
      cout << "   debug flag (Optional)   " << endl;
      cout << " --------------------------------------------- " << endl;
      exit(-1);
   }
//    string tmp(argv[6],strlen(argv[6]));
//    for (int i=7;i<argc;i++){
//      string opt(argv[i],strlen(argv[i]));
//      if (opt=="--noplot") lplot=false;
//      if (opt=="--num")    lnum=true;
//    }
//    filetuning = tmp;

//    chi2calib t(argv[1],argv[2],argv[3]);
//    std::string s(argv[5]);
//    double cut; istringstream is(s); is>>cut;
//    t.Loop(argv[4],cut);  
//    if (lplot) app.Run(true);
//    return 0;
// */


std::cout << " --------------------------------------------- " << std::endl;
   std::cout << " Analyze " << std::endl;
   string fileName(argv[1]);
   std::cout << " File name " << fileName << std::endl;

   string outFileName;
   size_t lastdot = fileName.find_last_of(".");
   if(lastdot!=std::string::npos) outFileName = fileName.substr(0,lastdot) + ".bin";
   else  outFileName = fileName + ".bin";
   if(argc>2) { outFileName=argv[2];}
   std::cout << " Out file name " << outFileName << std::endl;

   std::string side("");
   if(argc>3) side = argv[3];
   std::cout << " Side " << side << std::endl;
   
   int max = -1;
   if(argc>4) { std::string s=argv[4]; istringstream is(s); is>>max; }
   std::cout << " max # of tracks " << max << std::endl;
   
   int debug = 0;
   if(argc>5) { std::string s=argv[5]; istringstream is(s); is>>debug; }
   std::cout << " debug " << debug << std::endl;
   
   
   // Start X11 view
   TApplication theApp("App",NULL,NULL);
   theApp.SetReturnFromRun(true);
   
   MilleParser mp(fileName,outFileName,debug);
   
   mp.Analyze(side,max);

   theApp.Run();

   return 0;



}
