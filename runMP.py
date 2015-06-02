#!/usr/bin/python
import argparse, subprocess, sys, os.path, re

pedeBin = 'MillepedeII/pede'
paramMapFile = 'hpsSvtParamMap.txt'
global paramMap
paramMap= {}

class Parameter:
    def __init__(self, i,val,active,error=None):
        self.i = i
        self.name = getSensorName(i)
        self.val = val
        self.active = active
        self.error=error
    @classmethod
    def fromstr(cls,s):
        i = int(s.split()[0])
        val = float(s.split()[1])
        active = float(s.split()[2])
        if(len(s.split())>4):
            error = float(s.split()[4])
        else:
            error = None
        return cls(i,val,active,error)
    def toString(self):
        s = '%5d %10f %10f' % (self.i, self.val, self.active)
        if self.error!=None:
            s += '    %f' % self.error
        s += ' %s' % self.name
        return s


def initParamMap():
    try:
        f = open(paramMapFile,'r')
    except IOError:
        print 'Cannot open ', paramMapFile
        sys.exit(1)
    else:
        for line in f.readlines():
            if 'MilleParameter' in line:
                continue
            paramMap[int(line.split()[0])] = line.split()[1]
        print 'Initialized param map with ', len(paramMap), ' parameters'
        #for k,v in paramMap.iteritems():
        #    print k,' ', v
        f.close()

def getSensorName(i):
    if not bool(paramMap):
        initParamMap()        
    if i in paramMap:
        return paramMap[i]
    else:
        print 'Cannot find sensor for param ', i
        sys.exit(1)


def getMinimStr(filename):
    s = ""
    try:
        f_min = open(filename,'r')
    except IOError:
        print 'cannot open ', filename
    else:
        for l in f_min.readlines():
            s += l
        f_min.close()
    return s

def getDefaultParams():
    pars = []
    for h in range(1,3):
        for t in range(1,3):
            for d in range(1,4):
                for sensor in range(1,19):
                    if sensor<10:
                        s = "0" + str(sensor)
                    else:
                        s = str(sensor)
                    mpId = str(h) + str(t) + str(d) + s
                    p = Parameter(int(mpId),0.0,-1.0)
                    pars.append(p)
    return pars

def getParams(parfilename):
    pars = []
    if parfilename!=None:
        try:
            f_pars = open(parfilename,'r')
        except IOError:
            print 'cannot open ', parfilename
        else:
            for l in f_pars.readlines():
                if len(l.split())==3 or len(l.split())==5:
                    p = Parameter( int(l.split()[0]), float(l.split()[1]), float(l.split()[2]))
                    pars.append(p)
            f_pars.close()
    return pars


def updateFloatParams(pars,floats):
    print 'There are ',len(floats),' parameters to float'    
    for i in floats:
        pfound = None
        for p in pars:
            if p.i==int(i):
                pfound = p
        if pfound == None:
            print 'Cannot find parameter ', i
            sys.exit(1)
        if args.debug:
            print 'Float ', p.i
        pfound.active = 0
    return


def getModuleNrFromDeName(deName):
    m = re.search("module_L(\d)\S_", deName)
    if m==None:
        print 'Wrong module name format ', module
        sys.exit(1) 
    else:
        l = m.group(1)
        return int(l)


def getDir(param):
    i = int((param%1000)/100.0)
    if i==1:
        return 'u'
    elif i==2:
        return 'v'
    elif i==3:
        return 'w'
    else:
        print 'cannot extract dir from param ', param
        sys.exit(1)
def getType(param):
    return int((param%10000)/1000.0)
def getHalf(param):
    i = int((param%100000)/10000.0)
    if i==1:
        return 't'
    elif i==2:
        return 'b'
    else:
        print 'cannot extract half from param ',param
        sys.exit(1)


def getParamsFromModule(module):
    params = []       
    m = re.search("L([1-6])([tb])_([uvw])", module)
    if m==None:
        print 'Wrong module name format ', module, '. Should be e.g. \'L4t_u\''
        sys.exit(1) 
    else:
        moduleNr = int(m.group(1))
        half = m.group(2)
        d = m.group(3)
        #print 'find param for ', module, ' ', moduleNr, ' ' , half, ' ' , d
        for k,v in paramMap.iteritems():
            loopNr = getModuleNrFromDeName(v)
            loopType = getType(k)
            loopHalf = getHalf(k)
            #print 'test ', k, ' ', loopNr, ' ', loopType, ' ', loopHalf
            # only u-dir translation for now
            if moduleNr == loopNr and getDir(k)==d and loopType==1 and half==loopHalf:
                params.append(k)
        if not bool(params):
            print 'Cannot find param  for module ', module
    return params

def updateParams(pars,otherparms,resetActive=True):
    print 'There are ',len(otherparms),' to update'
    parsnew = []
    for p in pars:
        pfound = None
        for op in otherparms:
            if p.i==op.i:
                pfound = op
        if pfound != None:
            if resetActive:
                pfound.active=-1
            parsnew.append(pfound)
        else:
            parsnew.append(p)
    return parsnew


def buildSteerFile(name,inputfile,pars,minimStr):
    try:
        f = open(name,'w')
    except IOError:
        print 'cannot open file ', name
        return False
    else:
        f.write("CFiles\n")
        f.write(inputfile + "\n")

        f.write("\nParameter\n")
        for p in pars:
            f.write(p.toString() + "\n")
        
        f.write("\n\n")
        f.write(minimStr)
        f.close()        
        return True


def printEigenInfo():
    status = subprocess.call("cat millepede.eve", shell=True)
    return

def printResResults():
    try:
        f = open('millepede.res','r')
    except IOError:
        print 'cannot open res file ' 
        return
    else:
        active=False
        for l in f.readlines():
            if active:
                if len(l.split())==5:
                    p  = Parameter.fromstr(l)
                    if p.active != -1.0:
                        delta = float(l.split()[3])
                        if delta==0.0:
                            print "%s NO change" % ( p.toString() )
                        else:
                            d = p.val-delta
                            if d==0.0:
                                print "%s change is %f " % ( p.toString(), delta)
                            else:
                                print "%s change is %f or %f percent" % ( p.toString(), delta, delta/(d)*100.0)
            
            if 'Parameter' in l:
                active=True
    return


def printResults():
    printEigenInfo()
    printResResults()

def saveResults(inputfilename, name):
    status = subprocess.call("cp millepede.res " + " millepede-" + os.path.splitext(os.path.basename(inputfilename))[0] + "-" + name + ".res", shell=True)
    status = subprocess.call("cp millepede.eve " + " millepede-" + os.path.splitext(os.path.basename(inputfilename))[0] + "-" + name + ".eve", shell=True)
    status = subprocess.call("cp millepede.log " + " millepede-" + os.path.splitext(os.path.basename(inputfilename))[0] + "-" + name + ".log", shell=True)
    status = subprocess.call("cp millepede.his " + " millepede-" + os.path.splitext(os.path.basename(inputfilename))[0] + "-" + name + ".his", shell=True)



def runPede(filename):
    print "Clean up..."
    status = subprocess.call("rm millepede.res", shell=True)
    status = subprocess.call("rm millepede.eve", shell=True)
    status = subprocess.call("rm millepede.log", shell=True)
    status = subprocess.call("rm millepede.his", shell=True)
    
    s = pedeBin + " " + filename
    print 'Execute: ', s
    status = subprocess.call(s, shell=True)

def main(args):

    print "just GO"

    # initialize all the parameters into a list
    pars = getDefaultParams()
    print 'Found ', len(pars), 'default parameters'
    if args.debug:
        for p in pars:
            print p.toString()
    

    # check if there is a supplied parameter file.
    # this could be a result file from a previous fit
    inputpars = getParams(args.parameters)
    print 'Found ', len(inputpars), ' parameters to update'
    if args.parameters != None:
        if len(inputpars) != len(pars):
            print 'Wrong number of input parameters. Require all to be present in the input file, but not all active'
            sys.exit(1)
    
    if args.debug:
        for p in pars:
            print p.toString()

    # update the default parameters with the new input file
    # normally require that they become inactive here
    pars = updateParams(pars,inputpars,True)

    floatingPars = []

    # find the floating parameter for this fit
    if args.Modules is not None:
        for m in args.Modules:
            floatingPars.extend([str(mp) for mp in getParamsFromModule(m)])
    
    if args.float is not None:
        floatingPars.extend(args.float)

    updateFloatParams(pars,floatingPars)

    print 'List of floating parameters:'
    nfloats = 0
    for p in pars:
        if p.active==0:
            print p.toString()
            nfloats=nfloats+1

    if nfloats<1:
        print 'Something is wrong. At least one parameter need to be floating before running.'
        sys.exit(1)
    

    # get MP minimization settings
    minimStr = getMinimStr(args.minimization)

    # build the actual steering file
    name = "steer.txt"
    ok = buildSteerFile(name,args.inputfile,pars,minimStr)
    if not ok:
        print "Couldn't build steering file"
        sys.exit(1)

    # run the fit
    runPede(name)

    # print results
    printResults()

    # save results to a specific name if supplied
    if args.name != None:
        saveResults(args.inputfile, args.name)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MP help script')
    parser.add_argument('-i','--inputfile', required=True, help='List of parameters to float')
    parser.add_argument('-f','--float', nargs='+', help='List of MP parameters to float')
    parser.add_argument('-M','--Modules', nargs='+', help='List of modules to float, e.g. L3b L5b')
    parser.add_argument('-p','--parameters', help='Default parameters')
    parser.add_argument('-m','--minimization', default='steering/steer_minimization_template.txt', help='Default minimization settings')
    parser.add_argument('-d','--debug', action='store_true', help='Debug flag')
    parser.add_argument('-n','--name', help='If given output files will get tagged by this name.')
    args = parser.parse_args()
    print args


    main(args)
