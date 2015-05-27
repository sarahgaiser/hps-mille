#ifndef TrackAlignObj_h
#define TrackAlignObj_h
 
#include <string>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>
#include <map>



typedef std::map<int, std::map<int,float> >::iterator DerGLIt;

class TrackAlignObj {
 public:
  TrackAlignObj();
  ~TrackAlignObj() {};
  void clear();
  bool ok();

  void Layer(std::string lstr);
  int GetLayer();
 
  void AddDerLC(const std::vector<std::string>& lstr, const int& dir);

  void AddDerGL(const std::vector<std::string>& lstr, const int& dir,std::string side);
  float convert(const std::string& str);
  int convertInt(const std::string& str);
  void AddRes(const std::vector<std::string>& lstr,const int& dir);
  void GetDerLC(float * derlc,const int& axis);
  void GetDerGL(float * dergl,int * label,const int& axis);        
  int NGL();
  bool hasDirection(const int& dir);
  float GetRes(const int& axis);        
  float GetErr(const int& axis);
  void Layer(int l);
  void print();
  DerGLIt  GLIt() {return m_derGL.begin();};
  DerGLIt  GLItE() {return m_derGL.end();};
 private:
  
  int m_layer;
  std::map<int,float> m_res;
  std::map<int,float> m_reserr;
  std::map<int, std::vector<float> > m_derLC;  
  std::map<int, std::map<int,float> > m_derGL;  
  //float *derLc;
  
  
  
};

typedef std::vector<TrackAlignObj>::iterator TrkObjIt;


class Track {

 public:
 Track() {};
  ~Track() {};
  
  void clear() {
    side.clear();
    m_meas.clear();
  };
  TrkObjIt  GetIt() {return m_meas.begin();};
  TrkObjIt  GetItE() {return m_meas.end();};
  void Add(TrackAlignObj obj);
  int GetNMeasurements();
  bool ok();
  int NGL();
  std::string GetSide() {return side;};
  void SetSide(std::string s) {side=s;};
  void print();
  
 private:
  std::vector<TrackAlignObj> m_meas;
  std::string side; //0-bottom, 1-top
  
};



#endif
