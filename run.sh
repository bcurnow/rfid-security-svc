#!/bin/bash

currentDir=$(dirname $0)
currentDir=$(cd ${currentDir} && pwd)

export FLASK_APP=rfidsecuritysvc
export FLASK_ENV=development

pidFile=${currentDir}/flask.pid
logFile=${currentDir}/flask.log

if [ -f ${pidFile} ]
then
  echo "Flask is currently running, please use stop.sh to stop the current process or cleanup ${pidFile}" >&2
  exit 1
fi

flask run --host 0.0.0.0 > ${logFile} 2>&1 &
pid=$!

echo $pid > ${currentDir}/flask.pid
echo "Flask is running under pid ${pid}, logs are located at ${logFile}"
