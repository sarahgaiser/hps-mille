#!/usr/bin/python
### Print new HPS geometry file based on Millepede input ###
import compact_utils
import os
import sys
import argparse


def getArgs():
  parser = argparse.ArgumentParser(description='Print HPS geometry file')
  parser.add_argument('--compactfile','-c',required=True,help='Input file.')
  parser.add_argument('--millefiles','-m',nargs='+',help='Input Millepede files.')
  parser.add_argument('--outputname','-o',help='Name of output file')
  parser.add_argument('--debug','-d',type=int,default=0,help='Debug level.')
  args = parser.parse_args();
  #print args
  return args


if __name__ == '__main__':
    print 'Print new HPS geometry'
    args = getArgs()

    try:
        compact_file = open(args.compactfile,'r')
    except IOError:
        print args.compactfile,' compact file could not be opened'
        sys.exit(1)

    try:
        mille_files = []
        for fileName in args.millefiles:
            print 'Opening ', fileName
            mille_files.append(open(fileName,'r'))
    except IOError:
        print args.millefiles,' mille files could not be opened'
        sys.exit(1)
    
    try:
        if args.outputname == None:
            fileName, fileExt = os.path.splitext(os.path.basename(args.compactfile))
            compact_file_new = open(fileName + '_new' + fileExt,'w')
        else:
            compact_file_new = open(args.outputname,'w')
    except IOError:
        print ' Problem opening output file'
        sys.exit(1)
    
    params = compact_utils.getParameters(mille_files)

    print 'Found ',len(params), ' new parameters to be added'

    if len(params) > 0:
        try:
            compact_utils.writeNewCompact(compact_file,compact_file_new,params);        
        except IOError,e:
            sys.exit('cannot write files ' + e)
        except Exception,e:
            sys.exit('files werent opened or other general problem?')
    else:
        print 'no parameters found, do nothing'
    
    print 'close files.'
    compact_file_new.close()
    compact_file.close()    
    [f.close() for f in mille_files]
    print 'done.'
