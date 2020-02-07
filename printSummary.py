#!/usr/bin/python

import argparse, subprocess, sys, os.path, re
import utils
sys.path.append('pythonutils')
import compareRootHists
from ROOT import TGraph, TCanvas, TH1F, TLegend, gPad, TH2F, TLine


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
        h.GetXaxis().SetLabelSize(0.018)
        h.GetYaxis().SetLabelSize(0.02)
        ip = ip + 1


def plotCmp(filenames):
    fname = filenames[0]
    for fnameloop in filenames:
        if fnameloop==fname:
            continue
        compareRootHists.main(fname,fnameloop,None,'truth',None,True)


def plotResCmp(filenames, legendlist, half,t,d,uflip):
    # assume 18 parameters possible
    c_sum = TCanvas('c_sum','c_sum',10,10,1500,1000)
    c_sum.SetBottomMargin(0.4)
    vals = {}
    icolor = 1
    istyle = 20
#    leg = TLegend(0.78,0.6,0.9,0.87)
    leg = TLegend(0.78,0.8,0.9,0.87)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    savename = ''
    h_sum_template = None
    pars_template = None
    count = 0
    maxVal =  -99999.
    minVal = 99999.9
    #maxVal =  0.05
    #minVal = -0.05
    for filename in filenames:
        if args.rejectfiles != None:
            if re.match(args.rejectfiles,filename) != None:
                print 'skip file ', filename, ' base on pattern ', args.rejectfiles
                continue
        if savename=='':
            savename = os.path.splitext(os.path.basename(filename))[0]
        run = utils.getRunNr(filename)
        print run
        savename += '-' + str(run)
        parsTmp = utils.getResResults(filename,False)
        pars = []
        for p in parsTmp:            
            sel = True
            if (half == 'top' and not utils.getHalf(p.i) == 't'): sel = False
            if (not half == 'top' and not utils.getHalf(p.i) == 'b'): sel = False
            if t != '' and utils.getType(p.i) != t: sel = False
            if d != '' and utils.getDir(p.i) != d: sel = False
            if args.rejectnames != None:
                if re.match(args.rejectnames,p.name) != None: sel = False
            if sel:
                print 'adding ', p.toString()
                pars.append(p)
        
        pars = sorted(pars,utils.cmpSensors)
        print 'Got ', len(pars), ' for ', filename, 
        h_sum = TGraph()
        i = 0
        for p in pars:
            if uflip and t == 't' and d == 'u' and not utils.isAxial(p.name): v = -1.0*p.val
            else: v = p.val
            print i, ' ', p.i, v
            h_sum.SetPoint(i,i,v)
            i = i + 1
            if v > maxVal: maxVal = v
            if v < minVal: minVal = v
        i = 0
        isize=1
        if(run==7798): 
          icolor=1
          istyle=22
          isize=1.5

        if(run==5784): 
          icolor=801
          istyle=20
          isize=1.5

        h_sum.SetMarkerStyle(istyle)
        h_sum.SetMarkerSize(isize)
        h_sum.SetLineColor(icolor)
        h_sum.SetMarkerColor(icolor)
        if len(vals)==0:
            pars_template = pars
        icolor=icolor+1
        istyle=istyle+1
        if icolor>7:
            icolor = 1
            istyle = 21
        if legendlist != None and len(legendlist) != 0:
            leg.AddEntry(h_sum,legendlist[count],'LP')        
        else:
            leg.AddEntry(h_sum,'%s'%run,'LP')        
        vals[filename] = h_sum
        count = count + 1    

    h_sum_template = TH2F('h_' + half,'h_' + half, len(pars_template),0,len(pars_template), 10, minVal*1.1, maxVal*1.1)
    h_sum_template.SetStats(False)
    if(half == 'top'):
        h_sum_template.SetTitle('Millepede corrections per sensor, top;;local translation/rotations (mm/rad)')
        h_sum.SetTitle('Millepede corrections per sensor, top;;local translation/rotations (mm/rad)')
    if(half == 'bot'):
        h_sum_template.SetTitle('Millepede corrections per sensor, bottom;;local translation/rotations (mm/rad)')
        h_sum.SetTitle('Millepede corrections per sensor, bottom;;local translation/rotations (mm/rad)')
    setBinLabelsHist(h_sum_template,pars_template)

    c_sum.cd()
    h_sum_template.Draw()
    iv = 0
    for k,v in vals.iteritems():
#        v.Draw('PL,same')
        v.Draw('P,same')
    leg.Draw()
    zeroline = TLine(0,0,108,0)
    zeroline.SetLineStyle(2)
    zeroline.Draw("same") 

    savename += '_' + half
    if t != '': savename += '_' + t 
    if d != '': savename += '_' + d 
    c_sum.SaveAs('c_sum_' + savename + '.png')

    ans = raw_input('press anything to continue')
    

def main(args):
    print "just GO"
    for f in args.files:
        if args.rejectfiles != None:
            if re.match(args.rejectfiles,f) != None:
                print 'skip file ', f, ' base on pattern ', args.rejectfiles
                continue
        utils.printResResults(f)
    if not args.noplots:
        if args.legend != None:
            if len(args.legend) != len(args.files):
                print '# legend rows and files differ ', len(args.legend), ' ', len(args.files)
                sys.exit(1)
        plotResCmp(args.files, args.legend, 'top',args.type,args.direction,args.uflip)
        plotResCmp(args.files, args.legend, 'bot',args.type,args.direction,args.uflip)
    return 0


    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MP summary script')
    parser.add_argument('-f','--files', nargs='+', required=True, help='Res files.')
    parser.add_argument('-n','--noplots', action='store_true', help='Dont plot anyting.')
    parser.add_argument('-r','--rejectfiles', help='Pattern to reject input files.')
    parser.add_argument('--rejectnames', help='Pattern to reject names.')
    parser.add_argument('-l','--legend', nargs='+', help='Optional legend separated by whitespace.')
    parser.add_argument('-t','--type', default='',help='translation t or rotation r')
    parser.add_argument('-d','--direction',default='', help='u,v or w')
    parser.add_argument('-u','--uflip', action='store_true', help='flip u translations')
    args = parser.parse_args()
    print args
    main(args)
