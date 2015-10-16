#!/usr/bin/python

import sys, os, utils, math

survey_meas_tu = 0.05


def getSurveyMeasurements(parMap):
    s = '\n!Survey constraints tu\n'
    for p, name in utils.paramMap.iteritems():
        if utils.getModuleNrFromDeName(name) == 0: continue
        if utils.getDir(p) == 'u' and utils.getType(p) == 't':
           s += '\nMeasurement %.1f %.3f\n' % (0.0, survey_meas_tu)
           s += '%s %.1f\n' % (p, 1.0)
    return s

def getBeamspotConstraints(parMap):
    s = '\n!Beamspot constraints\n'
    for d in ['u','v','w']:
        print 'd=',d
        for t in ['t','r']:
            for iAxial in range(2):
                active = False
                print 'iAx=',iAxial
                for p, name in utils.paramMap.iteritems():
                    print 'look at ', name, ' ', p
                    if utils.getModuleNrFromDeName(name) != 0: continue
                    if (utils.isAxial(name) and iAxial==0) or (not utils.isAxial(name) and iAxial==1): continue
                    if utils.getDir(p) == d and utils.getType(p) == t:
                        print 'found one',name, ' ', p
                        if not active:
                            print 'ACTUVATE'
                            s += 'Constraint 0.\n'    
                            s += '%s %.1f\n' % (p, 1.0)
                            active = True
                        else:
                            print 'ADD'
                            s += '%s %.1f\n' % (p, -1.0)
    return s



def getMeasurementZ0(parMap):
    s = ''
    # Constraint:  <z0>_top + dz0_top = <z0>_bot + dz0_bot
    # i.e.  dz0_top - dz0_bot = -1 * ( <z0>_top - <z0>_bot)
    # where <z0>_top is the measured mean
    # measured z0 for top and bottom
    mean_t = 0.1
    mean_b = 0.05
    target = -1.0* ( mean_t - mean_b )
    uncertainty = 0.05
    s += '\n#z0 top/bottom constraint\nMeasurement %.3f %.3f\n' % (target, uncertainty)

    # Calculate d_top
    for p, info in utils.paramMap.iteritems():
        if utils.getDir(p) == 'u' and utils.getType(p) == 't' and utils.getHalf(int(p)) == 't':
            # stereo sensor have a cos stereo angle penalty
            # axial and stereo sensor have u in opposite directions globally
            f = 1.0/12.0 # weight from each sensor layer
            if not utils.isAxial( utils.getSensorName(p) ):
                if utils.getModuleNrFromDeName( utils.getSensorName(p) ) <= 3: st = 0.1
                else: st = 0.05
                f = -1.0 / 12.0 / math.cos(st)
            s += '%s %.3f\n' % (p, f)

    # Calculate d_bot
    # NOTE the minus sign applied applied to the factor f
    for p, info in utils.paramMap.iteritems():
        if utils.getDir(p) == 'u' and utils.getType(p) == 't' and utils.getHalf(int(p)) == 'b':
            f = 1.0/12.0
            if not utils.isAxial( utils.getSensorName(p) ):
                if utils.getModuleNrFromDeName( utils.getSensorName(p) ) <= 3: st = 0.1
                else: st = 0.05
                f = -1.0 / 12.0 *math.sin(st)
            s += '%s %.3f\n' % (p, f)
    
    return s








def getMeasurementD0(parMap):
    # similar to z0 constraint above
    s = ''
    mean_t = 0.1
    mean_b = 0.05
    target = -1.0* ( mean_t - mean_b )
    uncertainty = 0.05
    s += '\n#d0 top/bottom constraint\nMeasurement %.3f %.3f\n' % (target, uncertainty)

    # Calculate d_top
    for p, info in utils.paramMap.iteritems():
        if utils.getDir(p) == 'u' and utils.getType(p) == 't' and utils.getHalf(int(p)) == 't':
            # stereo sensor have a sin stereo angle penalty
            # axial and stereo sensor have v in same directions globally
            # axial don't contribute
            f = 1.0/6.0 # weight from each sensor layer
            if not utils.isAxial( utils.getSensorName(p) ):
                if utils.getModuleNrFromDeName( utils.getSensorName(p) ) <= 3: st = 0.1
                else: st = 0.05
                f = f/ math.cos(st)
            s += '%s %.3f\n' % (p, f)

    # Calculate d_bot
    # NOTE the minus sign applied applied to the factor f
    for p, info in utils.paramMap.iteritems():
        if utils.getDir(p) == 'u' and utils.getType(p) == 't' and utils.getHalf(int(p)) == 'b':
            f = -1.0/6.0
            if not utils.isAxial( utils.getSensorName(p) ):
                if utils.getModuleNrFromDeName( utils.getSensorName(p) ) <= 3: st = 0.1
                else: st = 0.05
                f = f * math.sin(st)
            s += '%s %.3f\n' % (p, f)
    
    return s


if __name__ == '__main__':

    utils.initParamMap()

    f = open('constaints.txt','w')
    
    f.write( getSurveyMeasurements(utils.paramMap) )
    f.write( '\n\n' )
    f.write( getBeamspotConstraints(utils.paramMap) )
    f.write( '\n\n' )
    #f.write( getMeasurementZ0( utils.paramMap ) )
    #f.write( '\n\n' )
    #f.write( getMeasurementD0( utils.paramMap ) )
    
    f.close()
