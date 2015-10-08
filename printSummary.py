#!/usr/bin/python

import argparse, subprocess, sys, os.path, re
import utils
sys.path.append('pythonutils')
import compareRootHists
from ROOT import TGraph, TCanvas, TH1F, TLegend, gPad, TH2F


def setBinLabels(gr,pars):
    #h = gr
    h = gr.GetHistogram()
    print 'setBinLabels ', len(pars)
    ip = 1
    for p in pars:
        b = h.FindBin(ip)
        print 'ip ', ip, ' b ', b ,': ' , p.toNiceString()
        h.GetXaxis().SetBinLabel(b, p.name + '(' + str(p.i) + ')')
        ip = ip + 1

def setBinLabelsHist(gr,pars):
    h = gr
    #h = gr.GetHistogram()
    print 'setBinLabels ', len(pars)
    ip = 0
    for p in pars:
        b = h.GetXaxis().FindBin(ip)
        print 'ip ', ip, ' b ', b ,': ' , p.toNiceString()
        h.GetXaxis().SetBinLabel(b, p.name + '(' + str(p.i) + ')')
        ip = ip + 1


def plotCmp(filenames):
    fname = filenames[0]
    for fnameloop in filenames:
        if fnameloop==fname:
            continue
        compareRootHists.main(fname,fnameloop,None,'truth',None,True)


def plotResCmp(filenames):
    # assume 36 parameters possible
    c_sum = TCanvas('c_sum','c_sum',10,10,1000,800)
    c_sumNZ = TCanvas('c_sumNonZero','c_sumNonZero',10,10,1000,800)
    c_sum.SetBottomMargin(0.45)
    c_sumNZ.SetBottomMargin(0.45)
    vals = {}
    valsNZ = {}
    icolor = 1
    istyle = 20
    leg = TLegend(0.78,0.6,0.9,0.87)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    savename = ''
    h_sum_template = None
    h_sumNZ_template = None
    for filename in filenames:
        if args.reject != None:
            if re.match(args.reject,filename) != None:
                print 'skip file ', filename, ' base on pattern ', args.reject
                continue
        if savename=='':
            savename = os.path.splitext(os.path.basename(filename))[0]
        run = utils.getRunNr(filename)
        print run
        savename += '-' + str(run)
        pars = utils.getResResults(filename,False)
        parsNZ = utils.getResResults(filename,True)
        print 'Got ', len(pars), ' for ', filename, 
        print 'Got ', len(parsNZ), ' nonzero for ', filename
        h_sum = TGraph()
        h_sumNZ = TGraph()
        i = 0
        maxVal =  0.11
        minVal = -0.11
        for p in pars:
            #print binmap[p.name], ' ', p.val
            h_sum.SetPoint(i,i,p.val)
            i = i + 1
            #if p.val > maxVal: maxVal = p.val
            #if p.val < minVal: minVal = p.val
        i = 0
        for p in parsNZ:
            h_sumNZ.SetPoint(i,i,p.val)
            i = i + 1
        h_sum.SetMarkerStyle(istyle)
        h_sum.SetMarkerSize(1.0)
        h_sum.SetLineColor(icolor)
        h_sum.SetMarkerColor(icolor)
        h_sumNZ.SetMarkerStyle(istyle)
        h_sumNZ.SetMarkerSize(1.0)
        h_sumNZ.SetLineColor(icolor)
        h_sumNZ.SetMarkerColor(icolor)
        if len(vals)==0:
            c_sum.cd()
            h_sum_template = TH2F('h_'+h_sum.GetName(),'h_'+h_sum.GetName(),h_sum.GetN(),0,h_sum.GetN(),10,minVal,maxVal)
            h_sum_template.SetStats(False)
            h_sum_template.Draw('hist')
            h_sum_template.SetTitle('Millepede corrections per sensor;;local translation/rotations (mm/rad)')
            h_sum.Draw('PL,same')
            c_sumNZ.cd()
            h_sumNZ_template = TH2F('h_'+h_sumNZ.GetName(),'h_'+h_sumNZ.GetName(),h_sumNZ.GetN(),0,h_sumNZ.GetN(),10,h_sumNZ.GetMinimum(),h_sumNZ.GetMaximum())
            h_sumNZ_template.SetStats(False)
            h_sumNZ_template.Draw('hist')
            h_sumNZ.Draw('PL,same')
            h_sum.SetTitle('Millepede corrections per sensor;;local translation/rotations (mm/rad)')
            h_sumNZ.SetTitle('Millepede corrections per sensor;;local translation/rotation (mm/rad)')
            setBinLabelsHist(h_sum_template,pars)
            setBinLabelsHist(h_sumNZ_template,parsNZ)
        else:
            c_sum.cd()
            h_sum.Draw('PL,same')
            c_sumNZ.cd()
            h_sumNZ.Draw('PL,same')

        icolor=icolor+1
        if icolor>7:
            icolor = 1
            istyle = 21
        leg.AddEntry(h_sum,'%s'%run,'LP')        
        vals[filename] = h_sum
        valsNZ[filename] = h_sumNZ
    c_sum.cd()
    c_sum.Update()
    leg.Draw()
    c_sumNZ.cd()
    leg.Draw()
    c_sum.SaveAs('c_sum_' + savename + '.pdf')
    c_sumNZ.SaveAs('c_sumNZ_' + savename + '.pdf')
    ans = raw_input('press anything to continue')
    

def main(args):
    print "just GO"
    for f in args.files:
        if args.reject != None:
            if re.match(args.reject,f) != None:
                print 'skip file ', f, ' base on pattern ', args.reject
                continue
        utils.printResResults(f)
    if not args.noplots:
        plotResCmp(args.files)
    return 0


    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MP summary script')
    parser.add_argument('-f','--files', nargs='+', required=True, help='Res files.')
    parser.add_argument('-n','--noplots', action='store_true', help='Dont plot anyting.')
    parser.add_argument('-r','--reject', help='Pattern to reject input files.')
    args = parser.parse_args()
    print args
    main(args)
