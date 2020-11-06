#!/bin/bash

currentDir=$(dirname $0)
currentDir=$(cd ${currentDir} && pwd)
pidFile=${currentDir}/flask.pid

if [ -f ${pidFile} ]
then
  pid=$(cat ${pidFile})
  ps -p ${pid} -o cmd | grep flask >/dev/null 2>&1
  if [ $? -eq 0 ]
  then
    echo "Killing ${pid}..."
    kill ${pid}
    rm ${pidFile}
  else
    echo "Pid ${pid} is not a Flask process" >&2
    rm ${pidFile}
  fi
else
  echo "Flask is not currently running, can't find ${currentDir}/flask.pid" >&2
fi
