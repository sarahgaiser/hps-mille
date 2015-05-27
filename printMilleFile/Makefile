
F_PATH=/usr/local/gfortran
CCOMP = g++-4.7
#CCOMP = ${F_PATH}/bin/gcc

CFLAGS = -Wall -O3
ROOTCFLAGS = $(shell root-config --cflags)
ROOTGLIBS = $(shell root-config --glibs)

MILLEDIR = MillepedeII
MILLEINC = -I$(MILLEDIR)
MILLEOBJ = $(MILLEDIR)/Mille.o

#INCLUDES = -I. $(MILLEINC) $(ROOTCFLAGS)
INCLUDES = -I. $(ROOTCFLAGS)


EXE = printMille
CXXLIST = MilleParser.C TrackAlignObj.C
OLIST   = $(patsubst %.C,%.o,$(CXXLIST))
HLIST   = $(patsubst %.C,%.h,$(CXXLIST)) 

#g++ -g -o runbjettrigcalib runbjettrigcalib.C BjetTrigCalib.C BjetTrigCalibAnal	

default: $(EXE) 


# Implicit rule to compile all classes
%.o : %.C %.h
#@echo "Compiling $< with CXXFLAGS: $(CXXFLAGS) INC: $(INCLUDES)"
	$(CCOMP) $(CFLAGS) $(INCLUDES) -c $< -o $*.o 

#-lgfortran -lm -lgomp -lz 

$(EXE): $(EXE).C $(OLIST)
	@echo "$(INCLUDES)"
	$(CCOMP) -g -o $(EXE) $(EXE).C $(INCLUDES) $(OLIST) $(ROOTGLIBS) $(CFLAGS) Mille.cc
#	$(CCOMP) -g -o $(EXE) $(EXE).C $(INCLUDES) $(OLIST) $(MILLEOBJ) $(ROOTGLIBS) $(CFLAGS) 
clean:
	rm -f *~
	rm -f *.o
	rm -f printmille
