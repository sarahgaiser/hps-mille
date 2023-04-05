javaFolder=/sdf/group/hps/users/sgaiser/src/hps-java
iter=$1
inputTag=$2
outputTag=$3
flip=$4
residuals=mpII_mis_residuals.res

python scripts/MisalignmentTool.py -j HPS_${inputTag}_${iter}_AlignmentTree.json
echo "python scripts/makeDetectorFromResiduals.py -i HPS_${inputTag}_${iter} -j ${javaFolder} -r ${residuals} -o ${outputTag} -c ${flip}"


python scripts/makeDetectorFromResiduals.py -i HPS_${inputTag}_${iter} -j ${javaFolder} -r ${residuals} -o ${outputTag} -c ${flip}
cd ${javaFolder}
#sh makeNewAlignmentIterationLCDD.sh iter1 ${outputTag}
cd -
