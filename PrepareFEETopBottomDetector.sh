#script for building a detector from the millepede top/bottom solutions

ITERATION="iter0"
OUTITERATION="iter1"

TAG="NewOPAngleBOT_m0_8mrad"
JAVADIR="/nfs/slac/g/hps2/pbutti/alignment/hps-java/"


TOPRESIDUALS="MPII_results_CMatrixConstrained_MomConstrain_MPII_10104_FEE_BOFFAlign_top/CMatrixConstrained-Mom1000kConstrained-millepede.res"
BOTRESIDUALS="MPII_results_CMatrixConstrained_MomConstrain_MPII_10104_FEE_BOFFAlign_bot/CMatrixConstrained-Mom1000kConstrained-millepede.res"



COMPACTNAME="CMatrixConstrained-Mom1000kConstrained-millepede"

#copy over the compact

cp ${JAVADIR}/detector-data/detectors/HPS_${TAG}_${ITERATION}/compact.xml  compact_${COMPACTNAME}.xml

#build the compact with top residuals


python buildCompact.py -c compact_${COMPACTNAME}.xml -j ${JAVADIR}/distribution/target/hps-distribution-4.5-SNAPSHOT-bin.jar -r ${TOPRESIDUALS} -t

#build the compact with bottom residuals

python buildCompact.py -c compact_${COMPACTNAME}.xml -j ${JAVADIR}/distribution/target/hps-distribution-4.5-SNAPSHOT-bin.jar -r ${BOTRESIDUALS} -t




#make the tag for the next iteration
DETDIR=${JAVADIR}/detector-data/detectors/HPS_${TAG}_${OUTITERATION}

cp -r ${JAVADIR}/detector-data/detectors/HPS_${TAG}_${ITERATION} ${DETDIR}

rm ${DETDIR}/*.lcdd
cp compact_${COMPACTNAME}.xml ${DETDIR}/compact.xml
echo "name: ${TAG}_${OUTITERATION}" > ${DETDIR}/detector.properties

cd ${JAVADIR}
sh makeNewAlignmentIterationLCDD.sh ${OUTITERATION} ${TAG}

cd - 

