import numpy as np
import math
from DerivativeConverter import DerivativeConverter
import argparse


def getArgs():
    parser = argparse.ArgumentParser(description="MPII misalignment creator")
    parser.add_argument("-j", "--json", help="The json file", default="./AlignmentTree.json")
    parser.add_argument("-i", "--input", help="Input misalignment", default="")
    parser.add_argument("-d", "--debug", help="Debug flag", action="store_true")
    args = parser.parse_args()
    print(args)
    return args


def Zspacing(dc, misfile, scaling=1e-4, volume="Top", debug=False):
    """Detector z spacing between axial and stereo; proportional to z_sensor"""

    print("Misalignment tool: Creating tw misalignment proportional to z_sensor")

    if volume == "Top":
        short_vol = "t"
    else:
        short_vol = "b"

    for orientation in ["axial", "stereo"]:
        moduleList = ["module_L" + str(i) + short_vol + "_halfmodule_" + orientation + "_sensor0_AV" for i in range(1, 5)]
        moduleList += ["doublesensor_" + orientation + "_L" + str(i) + "_" + volume + "_AV" for i in range(5, 8)]

        for module in moduleList:
            structure = dc.avs[module]
            origin = np.array(structure["origin"])
            zpos = origin[2]
            zmove = -zpos * scaling
            if debug:
                print(module, "[0.,0.," + str(zmove) + "0..0.,0." + "]")
            dc.generateMisalignments(module, misfile, [0., 0., zmove, 0., 0., 0.])


def Zspacing_const(dc, misfile, spacing=[], volume="Top", debug=False):
    """Detector z spacing between axial and stereo; constant by section: [L1,L2], [L3,L4], [L5,L6,L7]"""

    if len(spacing) == 1:
        spacing = [spacing[0], spacing[0], spacing[0]]
    if len(spacing) != 3:
        print("Wrong length of input spacing array! Need 1 or 3 inputs.")

    print("Misalignment tool: Creating tw misalignment in [[L1,L2], [L3,L4], [L5,L6,L7]]: " + spacing)

    if volume == "Top":
        short_vol = "t"
    else:
        short_vol = "b"

    for orientation in ["axial", "stereo"]:
        moduleList = ["module_L" + str(i) + short_vol + "_halfmodule_" + orientation + "_sensor0_AV" for i in range(1, 5)]
        moduleList += ["doublesensor_" + orientation + "_L" + str(i) + "_" + volume + "_AV" for i in range(5, 8)]

        for i in range(len(moduleList)):
            if i in [0, 1]:
                zmove = -spacing[0]/2
            elif i in [2, 3]:
                zmove = -spacing[1]/2
            else:
                zmove = -spacing[2]/2

            if debug:
                print(moduleList[i], "[0.,0.," + str(zmove) + "0.,0.,0." + "]")
            dc.generateMisalignments(moduleList[i], misfile, [0., 0., zmove, 0., 0., 0.])


def twist(dc, misfile, axis, scaling=5e-6, volume="Top", debug=False):
    """Twist misalignment of detector."""

    print("Misalignment tool: Creating twist misalignment")

    moduleList = ["ModuleL" + str(i) + "_" + volume + "_AV" for i in range(1, 8)]

    for module in moduleList:
        structure = dc.avs[module]
        # print("Structure origin in global frame")
        origin = np.array(structure["origin"])
        rotation = np.array(structure["rotation"])

        # Transform into the SVT Frame
        # The modules are oriented as axial sensors, so I can cheat
        # and build the matrix from the rotation matrix above
        # this should be roughly 30.5 mrad
        if debug:
            print(rotation)
        # !! Careful about the sign of this. This is local to global.
        svt_angle = rotation[0, 2]
        # !! Here I will change the sign to have the global rotation of the SVT wrt GLOBAL
        cos_svt = math.cos(-svt_angle)
        sin_svt = math.sin(-svt_angle)
        # And this is now the matrix from svt to global!
        svt2global = np.array([[cos_svt, 0, sin_svt], [0, 1, 0], [-sin_svt, 0, cos_svt]])
        global2svt = svt2global.transpose()

        # Get the origin in the SVT plane
        originT = origin.reshape(3, 1)

        origin_svt = global2svt.dot(originT)
        twist_angle = scaling * origin_svt[2, 0]

        cost = math.cos(twist_angle)
        sint = math.sin(twist_angle)

        # If the twist_angle is positive, rotate clockwise along SVT-Z axis
        rot = np.array([cost, -sint, 0, sint, cost, 0, 0, 0, 1])
        rot = rot.reshape(3, 3)

        if debug:
            print("TWIST ROTATION")
            print(rot)
            print("ORIGIN SVT")
            print(origin_svt)

        rot_origin_svt = rot.dot(origin_svt)

        if debug:
            print("ROTATED SVT")
            print(rot_origin_svt)

        # Now I have to compute the local changes.
        # I think it should be more correct to first correct the l2g rotation matrix by the angle and then
        # transform. (?)

        DeltaSVT = rot_origin_svt - origin_svt  # in the svt frame
        DeltaGlobal = svt2global.dot(DeltaSVT)  # in the global frame

        TwistedModuleRotation = np.dot(rot, rotation)

        # DeltaLocal  = (rotation.transpose()).dot(DeltaGlobal) # in the local frame
        DeltaLocal = (TwistedModuleRotation.transpose()).dot(DeltaGlobal)  # in the local frame

        # IMPORTANT. The Module W axis has the opposite sign wrt the SVT Z axis.
        # So I need to change sign here.
        Rw = -twist_angle

        # I might have done a sign error somewhere or the misalignment tool flips the sign, so I just
        # flip the sign in the following misalignment and everything is consistent.
        print(module, "[" + str(-DeltaLocal[0, 0]) + "," + str(-DeltaLocal[1, 0]) + ",0.0,0.0,0.0," + str(-Rw) + "]")
        dc.generateMisalignments(module, misfile, [-DeltaLocal[0, 0], -DeltaLocal[1, 0], 0., 0., 0., -Rw])


def main():
    print("Misalignment Tool")
    args = getArgs()
    dc = DerivativeConverter(args.json, False)

    misfile = open("misalignmentFile.txt", "w")
    misfile.write(" Parameter ! Generated misalignments\n")

    # dc.generateMisalignments("ModuleL7_Top_AV",
    #                          misfile,
    #                          [0.0,0.0,1.0,0.0,0.0,0.0])

    # dc.generateMisalignments("ModuleL7_Bot_AV",
    #                          misfile,
    #                          [0.0,0.0,1.0,0.0,0.0,0.0])

    #print("Calling twist...")
    #twist(dc,misfile,[0,0,1.],scaling=5e-6)

    Zspacing(dc, misfile, scaling=0.5e-2, debug=args.debug)
    Zspacing_const(dc, misfile, spacing=[0.1, 0.5, 1.0], volume="Bot", debug=args.debug)

    misfile.close()

    dc.LoadResults("misalignmentFile.txt")

    # Convert this in the HPS residuals
    SensorsList = [sname for sname in dc.avs.keys() if "sensor0" in sname and "ECal" not in sname]
    if args.debug:
        print(SensorsList)

    TotalCorrections = {}

    out = open("mpII_mis_residuals.res", "w")

    out.write(" Parameter  ! first 3 elements per line are significant (if used as input) \n")

    for sensor in SensorsList:
        TotalCorrections[sensor] = dc.computeParentCorrections(sensor)

    for sensor in SensorsList:
        if args.debug:
            print(sensor, TotalCorrections[sensor])
        for ilabel in range(len(dc.avs[sensor]["derivativeLabels"])):
            label = dc.avs[sensor]["derivativeLabels"][ilabel]
            out.write("     " + str(label) + "     " + str(round(TotalCorrections[sensor][ilabel], 4)) + "     -1.0000\n")

    out.close()


if __name__ == "__main__":
    main()
