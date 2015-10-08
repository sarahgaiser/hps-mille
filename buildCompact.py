#!/usr/bin/python
import argparse, subprocess, sys, os.path


def build(jarfile, compactfile, resfile, doText):
    print "Clean up..."
    name = "compact_" + os.path.splitext(os.path.basename(resfile))[0] + ".xml"
    
    s = "java -cp " + jarfile + " org.hps.svt.alignment.BuildMillepedeCompact -c " + compactfile + " " + resfile

    if doText:
        s += " -t"
    
    status = subprocess.call(s, shell=True)
    status = subprocess.call("cp compact_new.xml " + name, shell=True)
    status = subprocess.call("diff -w " + compactfile + " compact_new.xml | grep millepede", shell=True)



def main(args):

    print "just GO"

    build(args.jarfile,args.compactfile,args.resfile,args.t)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MP help script')
    parser.add_argument('-j','--jarfile', required=True, help='JAR file')
    parser.add_argument('-c','--compactfile', required=True, help='Compact XML file')
    parser.add_argument('-r','--resfile', required=True, help='Result file from MP')
    parser.add_argument('-t', action='store_true', help='Add correction as text string in compact.')
    args = parser.parse_args()
    print args


    main(args)
