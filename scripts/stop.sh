#!/bin/bash

rootDir=$(dirname $0)
rootDir=$(cd ${rootDir}/.. && pwd)
pidFile=${rootDir}/flask.pid

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
    echo "Pid ${pid} is not a Flask process, cleaning up ${pidFile}" >&2
    rm ${pidFile}
  fi
else
  echo "Flask is not currently running, can't find ${pidFile}" >&2
fi
