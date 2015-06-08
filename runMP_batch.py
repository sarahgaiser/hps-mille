#!/usr/bin/python

import sys, os, argparse, re, subprocess


def getArgs():
  parser = argparse.ArgumentParser(description='Run MP.')
  parser.add_argument('--run',action='store_true',help='Actually run this.')
  parser.add_argument('--files','-f',nargs='+',help='Input binary files.')
  
  args = parser.parse_args();
  print args
  return args


def getFloatModules(i):
    if i==0:
        return 'L2b_u L3b_u L4b_u L5b_u L2t_u L3t_u L4t_u L5t_u'
    elif i==1:
        return 'L1b_u L6b_u L1t_u L6t_u'
    elif i==2:
        return 'L1b_u L2b_u L4b_u L1t_u L2t_u L4t_u'
    else:
        print 'This iter ', i, ' is not allowed'
        sys.exit(1)



def run(fname):

    print '\n====\nRun on file ', fname

    name = ''
    for i in range(3):
        print 'Iteration ', i
        modules = getFloatModules(i)
        if name != '':
            pars = '-p millepede-' + os.path.splitext(os.path.basename(fname))[0] + '-' + name + '.res'
        else:
            pars = ''
        name += 'Iter' + str(i) 
        for m in modules.split():
            name += '-' + m
        
        cmd = 'python runMP.py -i ' + fname + ' -M ' + modules + ' ' + pars + ' --name ' + name
        print cmd
        if args.run:
            subprocess.call(cmd,shell=True)
    return 0

def main(args):

    print 'Run MP on ', len(args.files), ' input files'
    for fname in args.files:
        run(fname)
    

if __name__ == '__main__':
    args = getArgs()
    main(args)
