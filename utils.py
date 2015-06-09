import argparse, subprocess, sys, os.path, re

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
    def toNiceString(self):
        error = ''
        if self.error!=None:
            error = '%10f' % self.error
        s = '%40s %10f +- %s %5d' % (self.name, self.val, error, self.i)
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

def printEigenInfo(mpfile='millepede.eve'):
    status = subprocess.call("cat " + mpfile, shell=True)
    return


def getResResults(mpresfile='millepede.res', ignoreZero=False):
    result = []
    try:
        f = open(mpresfile,'r')
    except IOError:
        print 'cannot open res file ' 
        return result
    else:
        active=False
        for l in f.readlines():
            if active:
                p  = Parameter.fromstr(l)
                doIt = True
                if p.val==0. and ignoreZero:
                    doIt=False
                if doIt:
                    result.append(p)
            if 'Parameter' in l:
                active=True
    f.close()
    return result

def printResResults(mpresfile='millepede.res', ignoreZero=True):
    parameters = getResResults(mpresfile,ignoreZero)
    for p in parameters:
        print p.toNiceString()
    return

def printResults():
    printEigenInfo()
    printResResults()


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


def getRunNr(name):
    m = re.search('hps_00(\d{4})\S',name)
    if m==None:
        print 'Cannot find run number from ', name
        sys.exit(1)
    else:
        return int(m.group(1))

