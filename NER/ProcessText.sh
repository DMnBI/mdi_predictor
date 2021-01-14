DirPath=/home/yspark/program/textmining/NER/DBNER/TaggerOne-0.2.1

CP=${DirPath}/libs/taggerOne.jar
CP=${CP}:${DirPath}/libs/trove-3.0.3.jar
CP=${CP}:${DirPath}/libs/dragontool.jar
CP=${CP}:${DirPath}/libs/heptag.jar
CP=${CP}:${DirPath}/libs/fastutil-7.0.6.jar
CP=${CP}:${DirPath}/libs/jopt-simple-4.9.jar
CP=${CP}:${DirPath}/libs/commons-math3-3.5.jar
CP=${CP}:${DirPath}/libs/bioc.jar
CP=${CP}:${DirPath}/libs/stax-utils.jar
CP=${CP}:${DirPath}/libs/stax2-api-3.1.1.jar
CP=${CP}:${DirPath}/libs/woodstox-core-asl-4.2.0.jar
CP=${CP}:${DirPath}/libs/slf4j-api-1.7.20.jar
CP=${CP}:${DirPath}/libs/slf4j-simple-1.7.20.jar
PR="-Dorg.slf4j.simpleLogger.defaultLogLevel=debug -Dorg.slf4j.simpleLogger.showThreadName=false -Dorg.slf4j.simpleLogger.showLogName=false -Dorg.slf4j.simpleLogger.logFile=System.out"
REGULARIZATION=$1# format should either be "BioC" or "Pubtator"
FORMAT=$1 
MODEL=$2
INPUT=$3
OUTPUT=$4
CODE_PATH="${DirPaht}src/ncbi/taggerOne/"
AB3P_COMMAND="${DirPath}/identify_abbr"
AB3P_DIR="${DirPath}/Ab3P-v1.5"
TEMP="temp"
Ab3P_TIMEOUT=1000
OPT="--inputFilename ${INPUT}"
OPT="${OPT} --fileFormat ${FORMAT}"
OPT="${OPT} --outputFilename ${OUTPUT}"
OPT="${OPT} --modelInputFilename ${MODEL}"
OPT="${OPT} --useSentenceBreaker true"
OPT="${OPT} --abbreviationPostProcessingArgs 1|1|false"
OPT="${OPT} --consistencyPostProcessingArgs 10|1"
OPT="${OPT} --abbreviationSource ncbi.taggerOne.abbreviation.Ab3PAbbreviationSource|${AB3P_COMMAND}|${AB3P_DIR}|${TEMP}|${Ab3P_TIMEOUT}"
echo ${OPT}
java ${PR} -Xmx24G -Xms24G -cp ${CP} ncbi.taggerOne.ProcessText ${OPT}
