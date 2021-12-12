from DerivativeConverter import DerivativeConverter
import numpy as np


def main():
    print("Misalignment Tool")

    dc = DerivativeConverter("/nfs/slac/g/hps2/pbutti/alignment/hps-mille/paramMaps/AlignmentTree.json",True)
    
    misfile = open("misalignmentFile.txt","w")
    misfile.write(" Parameter ! Generated misalignments\n")
    
    #dc.generateMisalignments("Volume_Top",
    #                         misfile,
    #                         [0.1,0.2,0.,0.,0.,0.])
    
    
    #VOLUME TOP 
    #Tu,Tv recoverable (BS constraint is necessary)
    #Rv not recoverable
    #Rw not recoverable
    #Tz
    #dc.generateMisalignments("Volume_Top",
    #                         misfile,
    #                         [0.0,0.0,0.4,0.000,0.000,0.000])
    
    
    # UChannel Rot Rv 0.5mrad
    dc.generateMisalignments("UChannelL14_Top_AV",
                             misfile,
                             [0.0,0.0,0.0,0.0,0.0005,0.0])
    
    misfile.close()
    
    dc.LoadResults("misalignmentFile.txt")

    #Convert this in the HPS residuals

    SensorsList = [sname for sname in dc.avs.keys() if "sensor0" in sname and "ECal" not in sname]
    print(SensorsList)
    
    TotalCorrections={}
    
    out = open("mpII_mis_residuals.res","w")

    out.write(" Parameter  ! first 3 elements per line are significant (if used as input) \n")
    
    for sensor in SensorsList:
        TotalCorrections[sensor] = dc.computeParentCorrections(sensor)
        
    for sensor in SensorsList:
        print(sensor,TotalCorrections[sensor])
        for ilabel in range(len(dc.avs[sensor]["derivativeLabels"])):
            label = dc.avs[sensor]["derivativeLabels"][ilabel]
            out.write("     "+str(label)+"     "+str(round(TotalCorrections[sensor][ilabel],4)) +"     -1.0000\n")
        
    out.close()








if __name__=="__main__":
    main()
