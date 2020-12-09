#!/bin/bash

rootDir=$(dirname $0)
rootDir=$(cd ${rootDir}/.. && pwd)

export FLASK_APP=rfidsecuritysvc
export FLASK_ENV=development

cd ${rootDir}

formatted_args=""

for arg in "$@"
do
  if [[ ${arg} == *[[:space:]]* ]]
  then
    formatted_args="${formatted_args}\"${arg}\" "
  else
    formatted_args="${formatted_args}${arg} "
  fi
done
bash -c "/usr/local/bin/flask ${formatted_args}"
