#ifndef MilleParser_h
#define MilleParser_h

#include <string>




class MilleParser {

 public:
  
  MilleParser(std::string fileName,std::string outFileName, int debug=0);
  ~MilleParser();

  void Analyze(std::string useSide, int max);
  void AnalyzeNew(std::string useSide, int max);

 private:

  std::string m_fileName,m_outFileName;
  int m_debug;
  //Mille* m_mille;

};







#endif
