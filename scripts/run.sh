#!/bin/bash

rootDir=$(dirname $0)
rootDir=$(cd ${rootDir}/.. && pwd)

export FLASK_APP=rfidsecuritysvc
export FLASK_ENV=development

pidFile=${rootDir}/flask.pid
logFile=${rootDir}/flask.log

if [ -f ${pidFile} ]
then
  echo "Flask is currently running, please use stop.sh to stop the current process or cleanup ${pidFile}" >&2
  exit 1
fi

flask run --host 0.0.0.0 > ${logFile} 2>&1 &
pid=$!

echo $pid > ${pidFile}
echo "Flask is running under pid ${pid}, logs are located at ${logFile}"
