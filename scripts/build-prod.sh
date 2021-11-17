#!/bin/bash

rootDir=$(dirname $0)
rootDir=$(cd ${rootDir}/.. && pwd)
imageName=$(cd ${rootDir} && basename $(pwd))

docker image build \
  --platform linux/arm/v6 \
  -t ${imageName}:production  \
  ${rootDir}
