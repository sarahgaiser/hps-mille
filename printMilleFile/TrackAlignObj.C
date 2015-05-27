#include "TrackAlignObj.h"
#include <cstdlib>
#include <math.h>


void Track::Add(TrackAlignObj obj) {
  TrkObjIt it = GetIt();
  TrkObjIt itE = GetItE();
  for(;it!=itE;++it) {
    if(it->GetLayer()==obj.GetLayer()) {
      std::cout << "ERROR trying to add existing layer " << obj.GetLayer() << std::endl;
      exit(1);
    }
  }
  m_meas.push_back(obj);
}

int Track::GetNMeasurements() {return int(m_meas.size());}

void Track::print() {
  std::cout << "----- START OF TRACK -----" << std::endl;
  std::cout << " Half: " << side << std::endl;  
  std::cout << " # measurements " << GetNMeasurements() << std::endl;
  TrkObjIt it = GetIt();
  TrkObjIt itE = GetItE();
  for(;it!=itE;++it) {
    it->print();
  }
  std::cout << "----- END OF TRACK -----" << std::endl;
  
}

bool Track::ok() {
  if(GetNMeasurements()<=0) {
    std::cout << "this track had wrong nr of measurments \"" << GetNMeasurements() << "\" " << std::endl;
    return false;
  }
  if(side!="top" && side!="bottom") {
    std::cout << "track::ok(): this side \"" << side << "\" " << (side!="top")<< "," << (side!="top") <<" is not valid." << std::endl;
    return false;
  }
  TrkObjIt it = GetIt();
  TrkObjIt itE = GetItE();
  int n = it->NGL();
  for(;it!=itE;++it) {
    if(!it->ok()) {
      return false;
    }
    if(n!=it->NGL()) {
      std::cout << "ngl " << it->NGL() << " (should be "<< n <<") not ok for layer " << it->GetLayer() << std::endl;
      return false;
    }
  }
  return true;
}

int Track::NGL() {
  TrkObjIt it = GetIt();
  TrkObjIt itE = GetItE();
  int n = it->NGL();
  //cross-check!
  for(;it!=itE;++it) {
    if(n!=it->NGL()) {
      std::cout << "ERROR: obj at layer " << it->GetLayer() << " has " << it->NGL() << " while first obj had " << n << std::endl; 
      exit(1);
    }
  }
  return n;
}



TrackAlignObj::TrackAlignObj() {
    //derLC = new float
    clear();
  }
  void TrackAlignObj::clear() {
    m_layer = -1;
    m_res.clear();
    m_reserr.clear();
    m_derLC.clear();
    m_derGL.clear();
    
  }
  bool TrackAlignObj::ok() {
    //check layer
    if(m_layer<0) {
      std::cout << "This layer " << m_layer << " is not ok" << std::endl;
      return false;
    }

    // if(m_res.size()!=3) return false;
    // if(m_reserr.size()!=3) return false;
    
    //check that there is an error on each residual
    if(m_res.size()!=m_reserr.size()) {
      std::cout << "This residual sizes are not ok  " << m_res.size() << "," << m_reserr.size() << std::endl;
      return false;
    }
    
    //check that the local derivatives are there
    for(std::map<int,float>::const_iterator i=m_res.begin();i!=m_res.end();++i) {
      if(m_derLC[i->first].size()!=5) {
	std::cout<<"local derivative for direction " << i->first << " has size " << m_derLC[i->first].size() << " (should be 5?)" <<std::endl;
	return false;
      }
    }

    
    //if(m_derGL.size()!=3) return false;

    return true;
  }

bool TrackAlignObj::hasDirection(const int& dir) {
  std::map<int,float>::const_iterator found = m_res.find(dir);
  return found==m_res.end() ? false : true;  
}



  void TrackAlignObj::Layer(std::string lstr) { 
    std::istringstream iss(lstr);
    iss>>m_layer;
  }
  int TrackAlignObj::GetLayer() { return m_layer;}
  

  void TrackAlignObj::AddDerLC(const std::vector<std::string>& lstr, const int& dir) {    
    /* std::cout << "ERROR adding LC " << std::endl;  */
    /* std::cout << "dir = " << dir << " lstr:" << std::endl; */
    /* for(size_t i=0;i!=lstr.size();++i) std::cout << " " << lstr.at(i); */
    /* std::cout << std::endl; */
    /* print(); */
    /* exit(1); */
    if(lstr.size()!=2) {
      std::cout << "WARNING trying to add GderLC but size is wrong, might be end of file!" << std::endl;
      return;
    }
    if(m_derLC[dir].size()>4) {
      std::cout << "ERROR size" << std::endl; print(); exit(1);
    }    
    m_derLC[dir].push_back(convert(lstr[1]));
  }

void TrackAlignObj::AddDerGL(const std::vector<std::string>& lstr, const int& dir, std::string side) {    
    // if(m_derGL.find(dir)!=m_derGL.end()) {
    //   std::cout << "ERROR already has global dir " << dir << std::endl; 
    //   print();
    //   exit(1);
    // }
    if(lstr.size()!=3) {
      std::cout << "WARNING trying to add GL but size is wrong, might be end of file!" << std::endl;
      return;
    }

    int label = convertInt(lstr[2]);
    int int_side = label/(int) pow(10,4) % 10;
    std::string str_side = int_side==1? "top" : "bottom";
    if(str_side!=side) {
      std::cout << "ERROR gl side  " << str_side << " ("<<side<<") for GL but track is " << side << std::endl; exit(1);
      
    }

    if(m_derGL[dir].find(label)!=m_derGL[dir].end()) {
      std::cout << "ERROR gl dir " << dir << " already has label " << label << std::endl; print(); exit(1);
    }    
    m_derGL[dir][label] = convert(lstr[1]);
  }
  
  float TrackAlignObj::convert(const std::string& str) {
    float x;
    std::istringstream issss(str);
    issss>>x;
    return x;
  }

  int TrackAlignObj::convertInt(const std::string& str) {
    int x;
    std::istringstream issss(str);
    issss>>x;
    return x;
  }
  
  void TrackAlignObj::AddRes(const std::vector<std::string>& lstr,const int& dir) {
    if(lstr.size()!=3) {
      std::cout << "WARNING trying to add res but size is wrong, might be end of file!" << std::endl;
      return;
    }
    m_res[dir] = convert(lstr[1]);
    m_reserr[dir] = convert(lstr[2]);    
  }
  
  
  void TrackAlignObj::GetDerLC(float * derlc,const int& axis) {        
    
    for(size_t i=0;i<5;++i) {
      derlc[i]=m_derLC[axis][i];
    }
  }
  
  void TrackAlignObj::GetDerGL(float * dergl,int * label,const int& axis) {        
    int g=0;
    for(std::map<int,float >::const_iterator j=m_derGL[axis].begin();j!=m_derGL[axis].end();++j) {
      dergl[g] = j->second;
      label[g] = j->first;
      ++g;
    }
  }
  
  int TrackAlignObj::NGL() {
    //x-checkl that same nr of gl params for each existing res exist!
    size_t n = 0;
    std::map<int , std::map<int,float> >::const_iterator it=m_derGL.begin();
    std::map<int, std::map<int,float> >::const_iterator itE=m_derGL.end();
    n = it->second.size();
    for(;it!=itE;++it) {
      if(n != it->second.size()) {
	std::cout << "ERROR wrong nr of gl params for this trkalignobj" << std::endl;
	exit(1);
      }
    }
    return int(n);
  }

  float TrackAlignObj::GetRes(const int& axis) {        
    return m_res[axis];
  }
  float TrackAlignObj::GetErr(const int& axis) {        
    return m_reserr[axis];
  }
  
  
  void TrackAlignObj::Layer(int l) { m_layer=l;}
  
  void TrackAlignObj::print() {
    std::cout << "----- Alignment Local Object ----- " << std::endl;
    std::cout << "Layer " << m_layer << "" << std::endl;
    std::map<int,float>::const_iterator it =  m_res.begin();
    std::map<int,float>::const_iterator itE =  m_res.end();    
    std::cout << "Axis: ";
    for(;it!=itE;++it) std::cout <<  " " << it->first;
    std::cout << std::endl;
    it = m_res.begin();
    std::cout << "Res: ";
    for(;it!=itE;++it) std::cout <<  " " << it->second;
    std::cout << "" << std::endl;
    it =  m_reserr.begin();
    itE =  m_reserr.end();
    std::cout << "Err: ";
    for(;it!=itE;++it) std::cout << " " << it->second;
    std::cout << "" << std::endl;

    std::map<int, std::vector<float> >::const_iterator jt = m_derLC.begin();
    std::map<int, std::vector<float> >::const_iterator jtE = m_derLC.end();
    std::cout << "  derLC: " << std::endl; 
    for(;jt!=jtE;++jt) {
      std::cout << " axis " << jt->first <<": ";
      for(size_t i=0;i<jt->second.size();++i) std::cout << " " <<jt->second[i];
      std::cout << "" << std::endl;
    }
    
    std::cout << "  derGL: " << std::endl; 
    for(std::map<int, std::map< int,float > >::const_iterator j=m_derGL.begin();j!=m_derGL.end();++j) {
      std::cout << " axis " << j->first <<":" << std::endl;
      for(std::map< int,float >::const_iterator i=j->second.begin();i!=j->second.end();++i) {	
	printf("%8i  ",i->first);
      }
      std::cout << "" << std::endl;
      for(std::map< int,float >::const_iterator i=j->second.begin();i!=j->second.end();++i) {	
	printf("%5f  ",i->second);
      }
      std::cout << "" << std::endl;
    }
  }
