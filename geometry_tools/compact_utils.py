import os
import sys
import math

dimNameMap = {1:'x',2:'y',3:'z'}
typeNameMap = {1:'',2:'r'}
halfNameMap = {1:'t',2:'b'}

class Parameter:
    """Class holding a Millepede parameter"""
    def setValues(self,idn,value,presigma,diff,sigma):
        self.id = idn
        self.value = value
        self.presigma = presigma
        self.diff = diff
        self.sigma = sigma
    def setFromStr(self,str):
        vals = str.split()
        if len(vals) != 3 and len(vals) != 5:
            sys.exit('invalid input line: ' + str)
        idn = int(vals[0])
        if len(vals) == 5:
            self.setValues(int(vals[0]),float(vals[1]),float(vals[2]),float(vals[3]),float(vals[4]))
        else:
            self.setValues(int(vals[0]),float(vals[1]),float(vals[2]),-1.,-1.)
    def getHalf(self):
        return int(math.floor(self.id/1e4))
    def getType(self):
        h = self.getHalf() * 1e4       
        return int(math.floor((self.id - h)/1e3))
    def getDim(self):
        h = self.getHalf() * 1e4        
        t = self.getType() * 1e3       
        #print h,t
        return int(math.floor((self.id - h - t)/1e2))
    def getSensor(self):
        h = self.getHalf() * 1e4
        t = self.getType() * 1e3       
        d = self.getDim()  * 1e2      
        return int(self.id - h - t - d)
    def getConstantName(self):
        """ Translate between id and name in compact file """
        d = dimNameMap[self.getDim()]
        h = halfNameMap[self.getHalf()]
        t = typeNameMap[self.getType()]
        #print d, ' ' , h, ' ' , t
        return '%s%s%d%s_align' % (t,d,self.getSensor(),h)
    def getConstantStr(self):
        name = self.getConstantName()
        return '<constant name="%s" value="%f"/>' % ( name,  self.value)
         

def getParameters(mille_files):
    params = []
    for mille_file in mille_files:
        for line in mille_file:
            #print line
            if '!' not in line and not 'Parameter' in line:
                par = Parameter()
                par.setFromStr(line)
                params.append(par)
    return params


def writeNewCompact(compact_file,compact_file_new,params):
    """ Add parameters to new compact file """
    if compact_file.closed or compact_file_new.closed:
        raise Exception("Files not open")
    for line in compact_file:
        # Check if the parameters already exists in the compact and don't write them
        if '_align" value' in line:
            print 'skipping existing ', line.split('\n')[0]
            continue
        if '<constant name="final_' in line:
            print 'skipping existing final constant ', line.split('\n')[0]
            continue
        # do we write the params after this line?
        writeParamsHere = False
        if '<!-- alignment corrections -->' in line:
            writeParamsHere = True
        # do we write the final constants after this line?
        writeFinalConstantsHere = False
        if '<!-- final constants -->' in line:
            writeFinalConstantsHere = True
        compact_file_new.write(line)
        if writeParamsHere:
            for par in params:
                print 'adding new parameter: ', par.getConstantStr()
                compact_file_new.write('\t%s\n' % par.getConstantStr())
        if writeFinalConstantsHere:
            for par in params:
                name = par.getConstantName().split('_align')[0]
                print 'making final constant from : ', name, ' and ', par.getConstantName()
                compact_file_new.write('\t<constant name="final_%s" value="mod2_%s+%s"/>\n' % (name,name,par.getConstantName()))

            
