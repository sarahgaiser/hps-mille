#include "MilleParser.h"

#include <vector>
#include <map>
#include <cstdlib>

#include "Mille.h"
#include "TrackAlignObj.h"

#include "TApplication.h"
#include "TH1F.h"
#include "TFile.h"
#include "TCanvas.h"


//using namespace std;

std::string findType(std::string str) {

  std::string search_str ("_");
  size_t found = str.find(search_str);
  std::string type("");
  if(found!=std::string::npos) {
    type = str.substr(0,found);
    //std::cout << "found type " + type << " at: " << int(found) << std::endl;
  } else {
    std::cout << "ERROR this string has no valid type? " << str << std::endl;
    exit(1);      
  }
  return type;
}
      
int findDirection(std::string str, std::string type) {

  size_t found = str.find(type+"_");
  if(found!=std::string::npos) {
    //
  } else {
    std::cout << "ERROR in findDirection this string " << str << " has not type type " << type << std::endl;
    exit(1);      
  }
  size_t l = std::string(type+"_").length();
  std::string direction = str.substr(found+l,found+l+1);
  if(direction=="u") return 0; 
  else if(direction=="v") return 1; 
  else if(direction=="w") return 2; 
  else {
    std::cout << "ERROR this string has no valid direction? " << direction << std::endl;
    exit(1);      
  }
  return -1;
}
      




MilleParser::MilleParser(std::string fileName, std::string outFileName, int debug) {
 // :
 //  m_mille(outFileName.c_str(), true, false) {
  
  m_fileName = fileName;
  m_outFileName = outFileName;
  m_debug = debug;
  
  //m_mille = new Mille(outFileName.c_str(), true, false);
  //m_mille = new Mille("test.txt", true, false);
  
}

MilleParser::~MilleParser() {
  // std::cout << "Deleting mille" << std::endl;
  // delete m_mille;
  // std::cout << "After deleting mille" << std::endl;
}







void MilleParser::Analyze(std::string useSide, int max) {

  return AnalyzeNew(useSide,max);

}







void MilleParser::AnalyzeNew(std::string useSide, int max) {

  
  //Read file line by line
  std::ifstream fin;
  fin.open(m_fileName.c_str());
  if(m_debug) std::cout << "Opening file " << m_fileName << std::endl;


  if(!fin.good()) {
    std::cout << "ERROR file input not ok!" << std::endl;
    exit(1);
  }
  
  

  // Start X11 view
  //TApplication theApp("App",NULL,NULL);
  



  std::string direction[] = {"u","v","w"};
  TH1F * h_res[3][10];
  for(int i=0;i!=3;++i) {
    //TCanvas* c_res[3];
    std::ostringstream oss; 
    //oss << "c_" << direction[i];
    //c_res[i] = new TCanvas(oss.str().c_str(),oss.str().c_str(),10,10,700,500);
    //c_res[i]->Divide(2,5);
    for(int j=1;j!=11;++j) {
      std::ostringstream oss; 
      oss << "res_" << direction[i] << "_layer_" << j;
      std::string name = oss.str();
      //oss>>name;
      double xmin,xmax;
      if(i==0) {
	xmin=-1; xmax=1;
      } else if (i==1) {
	xmin=-100; xmax=100;      
      } else {
	xmin=-5; xmax=5;
      }

      h_res[i][j-1] = new TH1F(name.c_str(),name.c_str(),50,xmin,xmax);
    }
  }
  
  std::vector<Track> tracks;
  Track track;
  TrackAlignObj trkObj;
  std::string line;
  int c = 0;
  int ntrks = 0;
  
  while(!fin.eof()) {

    getline(fin,line);

    if(m_debug) std::cout << "Line: \"" << line << "\"  c=" << c  << " tracks " << tracks.size()  << std::endl;
    
    
    if(line=="") {
      std::cout << "This line is empty, this should be at the end of the file!?" << std::endl;
      if(fin.eof()) {
	std::cout << "Yupp" << std::endl;	
      } else {      
	std::cout << "Nope!" << std::endl;
	exit(1);
      }
      continue;
    }

    // Order is:
    // TRACK top/bottom
    // Layer
    // res_dir Res ErrorRes (local derivatives: 5 of them)
    // lc_dir dfdq (5 of them)
    // gl_dir dfdp (varying nr)
    //....
    //TRACK
    
    std::istringstream iss(line);
    std::vector<std::string> items;
    std::string item;
    
    //Split row into objects
    while(iss>>item) {      
      items.push_back(item);
    }
    

    if(items.size()==3) {
      //Is this a track?
      size_t found_track = items[0].find("TRACK");
      if(found_track!=std::string::npos) {
	//this is a new track
	
	if(ntrks%500==0) std::cout << "Processed " << ntrks << " tracks from text file" << std::endl;
	++ntrks;

	std::string side = items[1];
	std::string n = items[2];
	if(side!="top" && side!="bottom") {
	  std::cout << "ERROR track "<<n<<": this side \"" << side << "\" " << (side!="top")<< "," << (side!="top") <<" is not valid." << std::endl;
	  exit(1);
	}

	//std::cout << "This is a new "<< side<<" track!" << std::endl;
	
	//check if a temporary trkObj needs to be saved before clearing
	if(trkObj.GetLayer()!=-1) {
	  // save the existing one and clear if it's ok


	  if(trkObj.ok()) {
	    if(m_debug>1) std::cout << "Saving layer to existing track" << std::endl;
	    track.Add(trkObj);
	  } else {
	    std::cout << "ERROR align layer obj not ok " << std::endl;
	    std::cout << "at line: " << line << std::endl;
	    trkObj.print();
	    exit(1);
	  }
	}
	
	
	//check if a track exists
	if(track.GetNMeasurements() > 0 ) {
	  
	  if(track.ok()) {

	    bool correct_side = true;
	    if(useSide!="") {
	      correct_side = useSide==track.GetSide() ? true : false;
	    }
	   
	    if(correct_side) {
	      if(m_debug>1) std::cout << "There is an existing track, save this and clear" << std::endl;	    
	      if(m_debug) std::cout << "save " << track.GetSide() << " track" << std::endl;
	      tracks.push_back(track);
	      if(((int)tracks.size())%500==0) std::cout << "Added " << tracks.size() << " from text file" << std::endl;

	      if(max>0) {
		if(int(tracks.size())>=max) break;
	      }
	    }
	    
	  } 
	  else {
	    std::cout << "ERROR track not ok " << std::endl;
	    std::cout << "at line: " << line << std::endl;
	    track.print();
	    //exit(1);	    
	  }
	  if(m_debug>1) std::cout << "Clear track and layer object" << std::endl;	    

	  //clear it to start a new one
	  track.clear();
	  trkObj.clear();
	  
	}

	//Now we have a fresh new track object to add measurements to
	
	//Set the correct half of the tracker
	track.SetSide(side);
	
	// go to the next line
	c=1;
	continue;
      }
      else {
	if(m_debug>1) std::cout << "this was not a track line" << std::endl;
      }
    }
    else if(items.size()==1) {
	//No TRACK -> this must be a layer
	if(m_debug>1) std::cout << "This is should be a layer" << std::endl;	    

	//Check if it exists in the temporary track obj
	if(trkObj.GetLayer()!=-1) {
	  // save the existing one 
	  if(trkObj.ok()) {
	    if(m_debug>1) std::cout << "Saving the existing layer" << std::endl;	    
	    track.Add(trkObj);
	  } else {
	    std::cout << "ERROR align layer obj not ok " << std::endl;
	    std::cout << "at line: " << line << std::endl;
	    trkObj.print();
	    exit(1);
	  }

	  if(m_debug>1) std::cout << "Clear the layer object" << std::endl;	    
	  //clear it to start a new layer
	  trkObj.clear();
	}
	//Add the layer to the object and then go to next line
	if(m_debug>1) std::cout << "Add layer "<<items[0] << " to new layer object" << std::endl;	    
	trkObj.Layer(items[0]);
	c=2;
	continue;
    
    }
    else {
      if(m_debug>1) std::cout << "This is not a layer and not a new track line" << std::endl;
    }
    
    
    

    std::string type = findType(items[0]);
    int dir = findDirection(items[0],type);

    if(m_debug>1) std::cout << "This type \"" << type<< "\" (direction="<<dir<<") should be residual or der information" << std::endl;	    
    
    if(type=="res") {
      
      if(m_debug>1) std::cout << "Adding residuals" << std::endl;
      trkObj.AddRes(items,dir);
      

    }
    else if(type=="lc") {
      
      if(m_debug>1) std::cout << "Adding local ders" << std::endl;
      trkObj.AddDerLC(items,dir);
      
    }

    else if(type=="gl") {
      
      if(m_debug>1) std::cout << "Adding global ders" << std::endl;
      trkObj.AddDerGL(items,dir,track.GetSide());
      
    }
    
    //trkObj.print();
    ++c;
    
    
  }


  fin.close();


  std::cout << "Read " << tracks.size() << " tracks. Now put them in mille!" << std::endl;
  

  Mille* m_mille = new Mille(m_outFileName.c_str(), true, false);
  const int NLC = 5;
  float derLc[NLC];
  float * derGl = NULL;
  int * label = NULL;
  int NGL;

  std::map<int,int> labels;

  for(size_t t=0;t<tracks.size();++t) {
    
    if(((int)t)%1000==0 || m_debug) {
      std::cout << "Processing track " << t << std::endl;
      //tracks[t].print();
    }

    if(m_debug) std::cout << "Allocate new arrays, prev at  " << derGl << " , " << label  << std::endl;
    
    //Same nr of global parameters for each measurement direction for each track
    NGL = tracks[t].NGL();
    derGl = new float[NGL];
    label = new int[NGL];
    
    
    if(m_debug) std::cout << "NGL " << NGL << std::endl;
    
    TrkObjIt objIt  = tracks[t].GetIt();
    TrkObjIt objItE = tracks[t].GetItE();
    for(;objIt!=objItE;++objIt) {
      
      if(m_debug) std::cout << " add measurement on layer " << objIt->GetLayer() << std::endl;
      
      
      for(size_t idx=0;idx<3;++idx) {	
	
	
	if(!objIt->hasDirection(idx)) continue;

	if(m_debug)  std::cout << "direction " << idx << std::endl;
	
	
	float  rMeas = objIt->GetRes(idx);	
	float sigma = objIt->GetErr(idx);	
	
	
	objIt->GetDerLC(derLc,idx);
	
	
	objIt->GetDerGL(derGl,label,idx);


	//if(m_debug) 
	std::cout << "rMeas +- sigma " << rMeas << " +- " << sigma << " for layer =" << objIt->GetLayer() <<std::endl;
	if(m_debug) {
	  std::cout << "derLC: ";
	  for (int i=0;i!=5;++i) std::cout << " " << derLc[i];
	  std::cout << std::endl;
	}

	
	m_mille->mille(NLC,derLc,NGL,derGl,label,rMeas,sigma);
	
	for(int i=0;i<NGL;++i) {
	  ++labels[label[i]];
	}
	
	h_res[idx][objIt->GetLayer()-1]->Fill(rMeas);
	
	
	if(m_debug) {
	  
	  std::cout << "(layer="<<objIt->GetLayer()<<") axis " << idx << ":\n " << rMeas << "  +- " << sigma << "  h_res[idx][objIt->GetLayer()-1] " << h_res[idx][objIt->GetLayer()-1]  << std::endl;
	  for(int i=0;i!=NLC;++i) std::cout << " " << derLc[i];
	  std::cout << std::endl;
	  for(int i=0;i!=NGL;++i) std::cout << " " << derGl[i] << "("<<label[i]<<")  ";
	  std::cout << std::endl;	
	  
	}
	
	  if(m_debug) std::cout << "Added direction " << idx << " from layer " << objIt->GetLayer() << std::endl;
      } //direction 
      
      
      if(m_debug) std::cout << "Added measurements from obj with layer " << objIt->GetLayer() << std::endl;
    } // loop over all objects in the track
    
    if(m_debug) {
      std::cout << "deleting arrays" << std::endl;
    }
    delete [] derGl;
    delete [] label;
    
    // std::cout << labels.size() << " labels:" << std::endl;
    // for(std::map<int,int>::const_iterator it=labels.begin();it!=labels.end();++it) {
    //   std::cout << it->first << " " << it->second << std::endl;
    // }
    
    if(m_debug) {
      std::cout << "call mille end" << std::endl;
    }
    
    
    //Should be called for each local-fit object -> each track!?
    m_mille->end();
    
    if(m_debug) {
      std::cout << "after call mille end" << std::endl;
    }
    
    
    if(m_debug) std::cout << "Added " << track.GetNMeasurements() << " measurements from track " << t << std::endl;

  } // Loop over all tracks

  
  
  std::cout << "Deleting mille" << std::endl;
  delete m_mille;
  std::cout << "After deleting mille" << std::endl;
  
  
  //// Start X-Windows
  //theApp.Run();
  
  // TCanvas* can = new TCanvas("can","can",5,5,700,500);
  // can->Divide(2,2);
  // can->Update();
  // gPad->Update();

  TCanvas* c_res[3][10];
  std::string rootfilename = m_outFileName;
  size_t found = rootfilename.find(".");
  TFile* rootFile = new TFile((m_outFileName.substr(0,found)+".root").c_str(),"RECREATE");
  for(int i=2;i!=-1;--i) {
    //c_res[i]->Divide(5,5);
    //c_res[i]->Update();
    for(int j=1;j!=11;++j) {
      std::ostringstream oss; 
      oss << "c_" << direction[i] << "_" << j ;
      c_res[i][j-1] = new TCanvas(oss.str().c_str(),oss.str().c_str(),10,10,700,500);
      //c_res[i]->GetPad(j-1)->cd();
      
      c_res[i][j-1]->cd();
      //gPad = c_res[i]->cd(j-1); << std::endl;
      
      h_res[i][j-1]->SetFillStyle(1001);       
      h_res[i][j-1]->SetFillColor(kYellow);       
      h_res[i][j-1]->Draw();       
      // if(i==0 && j==0) {
      // 	can->cd(1);
      // 	h_res[i][j-1]->Draw();
      // 	gPad->cd();
      // 	gPad->Update();
      // }
      //if(i==0) {
      //c1->cd(j-1);
      //h_res[i][j-1]->Draw();       
      //}
      rootFile->cd();
      h_res[i][j-1]->Write();
      //std::ostringstream n;
      //n << "plots/" << h_res[i][j-1]->GetName() << ".jpg";
      //h_res[i][j-1]->SaveAs(n.str().c_str());       
    }
  }
  
  // std::cout << "Press anything to exit: ";
  // std::string s;
  // std::cin >>  s;
  

  //can->SaveAs("can.png");


   rootFile->Close();
   //delete rootFile;
  
  
  
  // for(int i=0;i!=3;++i) {
  //   for(int j=1;j!=11;++j) {
  //     delete h_res[i][j-1];
  //   }
  // }
  
  
  
  return;  
  
  
  }








    

