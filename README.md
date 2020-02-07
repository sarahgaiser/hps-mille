6 Feb 2020

# hps-mille

1. Compile Millepede:

```
cd MillepedeII 
make
```

2. Run Millepede once:

To run millepede on the output binary form GBL use the ```runMP.py``` script

```
cd /nfs/slac/g/hps2/phansson/software/hps-mille/
./runMP.py -i ../batch/output/hps_005796.evio.0-nominalAllevents/milleBinaryISN_hps_005796.evio.0.gbl.dat -M NAMES
```

The ```NAMES``` are a list coded as the following regexp:
L(1-6)[AS]?[hs]?[tb]_([tr])([uvw])
i.e. the ones with question mark is optional (and you get the inclusive sensors if not given).

Example:
-M L4Ah_rv # rotation around unmeasured direction for L4, axial, hole sensor.
-M L3_tu # translation in measured coord for L3 axial and stereo sensor

or you can run with the MP parameters instead if you want to (I prefer the human readable way):
./runMP.py -i ../batch/output/hps_005796.evio.0-nominalAllevents/milleBinaryISN_hps_005796.evio.0.gbl.dat -M parameters
v

eparametersf are a list of MP parameter IDs, e.g. 11101 is translation in measured direction for L1 top axial.

3. Run Millepede in iterations:
There is a gbatchh script that runs runMP.py over multiple input files with multiple iterations of millepede. 

Do a gdryh run without specifying e\runf to see what it will actually do:

cd /nfs/slac/g/hps2/phansson/software/hps-mille
./runMP_batch.py -f ../batch/output/hps_005796.evio.0-nominalAllevents/milleBinaryISN_hps_005796.evio.0.gbl.dat \-switch ID [\run]


where the switch is an integer that determines which floating settings MP will use. 

Use e-ff option to list the floating options to millepede. 

./runMP_batch.py -f ../batch/output/hps_005796.evio.0-nominalAllevents/milleBinaryISN_hps_005796.evio.0.gbl.dat -l

Run MP on  1  input files
2  options:

Option  0 :  L5u_L2u_2iterseach:
 Iteration  Floating
         0  L5b_u L5t_u
         1  L2b_u L2t_u
         2  L5b_u L5t_u
         3  L2b_u L2t_u

Option  0 :  L1-5_tu:
 Iteration  Floating
         0  L2b_tu L3b_utu L4b_tu L5b_tu L2t_tu L3t_tu L4t_tu L5t_tu


The options are hardcoded in the function:

initListOfFloatOptions

and it should be easy to add something new. 

The output will be stamped with the option enamef i.e. L5u_L2u_2iterseach and each iteration output will be saved (names become ugly but we can fix that later). 


4. Print a summary of a MP *.res output file:
cd /nfs/slac/g/hps2/phansson/software/hps-mille > ./printSummary.py
usage: printSummary.py [-h] -f FILES [FILES ...] [-n]


5. Create compact file.
There is a wrapper script to run the java converter in the hps-mille repo:
cd /nfs/slac/g/hps2/phansson/software/hps-mille/
./buildCompact.py 
usage: buildCompact.py [-h] -j JARFILE -c COMPACTFILE -r RESFILE
