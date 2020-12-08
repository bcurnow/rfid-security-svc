#!/bin/bash

rootDir=$(dirname $0)
rootDir=$(cd ${rootDir}/.. && pwd)

export FLASK_APP=rfidsecuritysvc
export FLASK_ENV=development

cd ${rootDir}


bash -c "/usr/local/bin/flask $(printf ' %q' "$@")"
