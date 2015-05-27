CCOMP = g++-4.7
CFLAGS = -Wall -O3
ROOTCFLAGS = #$(shell root-config --cflags)
ROOTGLIBS = #$(shell root-config --glibs)

#MILLEDIR = Mptwo
MILLEDIR = ../MillepedeII
MILLEINC = -I$(MILLEDIR)
MILLEOBJ = $(MILLEDIR)/Mille.o

INCLUDES = -I. $(MILLEINC) $(ROOTCFLAGS)


EXE = printMille

default: $(EXE) 


$(EXE): $(EXE).C 
	@echo "Compiling $@"
	g++-4.7 -g -o $(EXE) $(EXE).C Mille.cc -I.
#	g++-4.7 -g -o $(EXE) $(EXE).C $(MILLEINC) $(MILLEOBJ) -lgfortran -lm -lgomp -lz
clean:
	rm -f *~
	rm -f *.o
	rm -f printmille
