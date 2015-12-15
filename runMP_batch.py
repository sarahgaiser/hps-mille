#!/usr/bin/python

import sys, os, argparse, re, subprocess
import floatoptions

beamspot = False
beamspotConstraint = False
surveyConstraint = False


def getArgs():
  parser = argparse.ArgumentParser(description='Run MP.')
  parser.add_argument('--run',action='store_true',help='Actually run this.')
  parser.add_argument('--files','-f',nargs='+', required=True, help='Input binary files.')
  parser.add_argument('--listoptions','-l', action='store_true', help='List available defined floating options.')
  parser.add_argument('--switch','-s', type=int, help='Switch to change what patter of floating modules.')
  parser.add_argument('-b','--beamspot', action='store_true',help='Beamspot is included in the fit')
  parser.add_argument('--SC', action='store_true',help='Survey constraint')
  parser.add_argument('--BSC', action='store_true',help='Beamspot constraint')

  args = parser.parse_args();
  print args
  return args






def run(binaryfilenames, opt):

    print '\n====\nRun on files ', binaryfilenames
    binnames = [ os.path.splitext( os.path.basename(n) )[0] for n in binaryfilenames]
    binarynames = '-'
    binarynames = binarynames.join(binnames)
    
    filenames = ' '
    filenames = filenames.join(binaryfilenames)
    
    name = opt.getName()
    for i in range(opt.getNIter()):
        print 'Iteration ', i
        modules = opt.get(i)
        if name != opt.getName():
            pars = '-p millepede-' + binarynames + '-' + name + '.res'
        else:
            pars = ''
        name += 'Iter' + str(i) 

        # Add beamspot options
        bs = ''
        if beamspot: bs += ' --beamspot'
        if beamspotConstraint: bs += ' --BSC'
        if surveyConstraint: bs += ' --SC'
        print 'BS options: \"', bs, '\"'
        cmd = 'python runMP.py -i ' + filenames + ' -M ' + modules + ' ' + pars + ' --name ' + name + bs
        print cmd
        if args.run:
            subprocess.call(cmd,shell=True)
    return 0



def main(args):

    print 'Run MP on ', len(args.files), ' input files'
    floats = floatoptions.FloatOptions()
    if args.listoptions:
        floats.printlist()
        sys.exit(0)

    global beamspot
    global beamspotConstraint
    global surveyConstraint    
    beamspot = args.beamspot
    beamspotConstraint = args.BSC
    surveyConstraint = args.SC

    if args.switch==None:
        print 'Need to specify which option to run using the --switch'
        sys.exit(0)

    print 'Switch ', args.switch
    opt = floats.getoption(args.switch)
    if opt==None:
        print 'Couldnt find option for switch ', args.switch
        sys.exit(1)
    print opt.toString()

    run(args.files,opt)
    

if __name__ == '__main__':
    args = getArgs()
    main(args)
