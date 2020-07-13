from ROOT import *
import argparse,os,sys
from array import array

#This macro plots the corrections from a compact
#To know which global parameters need to be checked it uses the steering file used for computing the solution

colors  = [kBlue+2,kRed+2,kGreen-1,kYellow+2,kRed+2,kBlack,kAzure-2,kGreen-8,kOrange+3,kYellow+2,kRed+2,kBlue+2,kGreen-8,kOrange+3,kYellow+2,kRed+2,kBlue+2,kGreen-8,kOrange+3,kYellow+2,kRed+2,kBlue+2,kGreen-8,kOrange+3,kYellow+2,kRed+2,kBlue+2,kGreen-8,kOrange+3]


def getArgs():
    parser = argparse.ArgumentParser(description='Correction plotter script')
    parser.add_argument('-c','--compact', help='Compact to read the corrections from',default="")
    parser.add_argument('-o','--outDir',dest="outDir",help="Output dir",default="./CorrectionsResults/")
    parser.add_argument('-n','--name', dest="name",help='If given output files will get tagged by this name.')
    parser.add_argument('-s','--steering', dest="steering",help='Steering file to parse the floating parameters from',default="")
    parser.add_argument("-g",'--globals',nargs="+",dest="globals",help="List of global labels to plot",default="")

    args = parser.parse_args()
    print args 
    return args


def main():
    
    args = getArgs()
    
    if not os.path.exists(args.outDir):
        os.makedirs(args.outDir)
    
    if (args.steering == "" and args.globals==""):
        print "No steering file nor global list provided. Exiting."
        sys.exit()
            
    if (args.compact ==""):
        print "Provide compact file."
        sys.exit()
    
    compactFile = args.compact
    globals = args.globals

    print compactFile, globals
    
    correctionsMap = getCorrections(compactFile,globals)
    
    MakeValidationPlot(correctionsMap)
    

def getCorrections(compactFile,globals):
    
    corrs = {}
    
    cfile = open(compactFile)

    for line in cfile.readlines():
        for gl in globals:
            if gl in line:
                str_globs = ((line.split('value="'))[-1].split('"/>')[0]).split()
                print gl, str_globs
                
                corrs[gl] = str_globs
                pass
            pass
        pass
    
    cfile.close()
    return corrs


#Validation Plot for MC re-alignment. 
#Assumes that the first correction in the str_globs list is the initial value 
#(can be 0, for example, or something else)


def MakeValidationPlot(correctionsMap):
    
    graphs = {}
    #cumulative corrections (point i is the sum of i-1 and i
    graphsc = {}
    npoints = 0

    for key in correctionsMap.keys():
        npoints = len(correctionsMap[key])-1 
        target  = correctionsMap[key][0]
        x, y = array( 'd' ), array( 'd' )
        yc = array( 'd' )
        yc_value = 0.
        for ipoint in xrange(npoints):
            x_value = float(ipoint)
            y_value = float(correctionsMap[key][ipoint+1])
            
            yc_value += y_value
            
            x.append(x_value)
            y.append(y_value)
            yc.append(yc_value)
            pass
        
        
        print key,npoints,x,y 
        print key,npoints,x,yc 
        
        
        graphs[key]=[TGraph(npoints,x,y),float(target)]
        graphsc[key]=[TGraph(npoints,x,yc),float(target)]
        pass
    print graphs
    
    c = TCanvas()
    c.SetLeftMargin(0.15)
    c.cd()

    leg2 = TLegend(0.7,0.8,0.88,0.6)
    leg2.SetBorderSize(0)
    leg2.SetFillColor(0)
    leg2.SetTextSize(0.04)
    
    for ikey in xrange(len(graphs.keys())):
        key = graphs.keys()[ikey]
        
        if (ikey==0):
            graphs[key][0].SetTitle("")
            graphs[key][0].Draw("APL")
            graphs[key][0].GetYaxis().SetRangeUser(-0.08,0.08)
            graphs[key][0].GetYaxis().SetTitle("Alignment Correction Value [rad/mm]")
            graphs[key][0].GetXaxis().SetTitle("MPII Iteration")
            
        else:
            graphs[key][0].Draw("PLsame")


        graphs[key][0].SetLineWidth(2)
        graphs[key][0].SetLineColor(colors[ikey])
        graphs[key][0].SetMarkerColor(colors[ikey])
        
        leg2.AddEntry(graphs[key][0],key,"lpf")
    
    leg2.Draw()
            
    c.SaveAs("Validation_corrections.pdf")    

    
    c.cd()
    c.Clear()

    leg = TLegend(0.7,0.8,0.88,0.6)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.04)
    
    for ikey in xrange(len(graphs.keys())):
        key = graphsc.keys()[ikey]
        
        if (ikey==0):
            graphsc[key][0].SetTitle("")
            graphsc[key][0].Draw("APL")
            graphsc[key][0].GetYaxis().SetRangeUser(-0.08,0.08)
            graphsc[key][0].GetYaxis().SetTitle("Total Alignment Correction Value [rad/mm]")
            graphsc[key][0].GetXaxis().SetTitle("MPII Iteration")
        else:
            graphsc[key][0].Draw("PLsame")

        graphsc[key][0].SetLineWidth(2)
        graphsc[key][0].SetLineColor(colors[ikey])
        graphsc[key][0].SetMarkerColor(colors[ikey])

        
        leg.AddEntry(graphsc[key][0],key,"lpf")

    leg.Draw()
    line = TLine(0,0,npoints-1,0)
    line.SetLineColor(kRed)
    line.SetLineWidth(2)
    line.SetLineStyle(2)
    line.Draw("same")
    
    
    

    c.SaveAs("Validation_cumulative.pdf")    
   
if (__name__=="__main__"):
    main()
