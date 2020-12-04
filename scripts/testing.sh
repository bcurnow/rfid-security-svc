#!/bin/bash

currentDir=$(dirname $0)
currentDir=$(cd ${currentDir} && pwd)

${currentDir}/stop.sh && ${currentDir}/run.sh && cat ${currentDir}/../test.apikey && tail -f ${currentDir}/../flask.log
