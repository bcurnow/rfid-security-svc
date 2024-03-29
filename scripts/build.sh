#!/bin/bash

rootDir=$(dirname $0)
rootDir=$(cd ${rootDir}/.. && pwd)
imageName=$(cd ${rootDir} && basename $(pwd))

docker image build \
  --target dev_image \
  --build-arg USER_ID=$(id -u ${USER}) \
  --build-arg GROUP_ID=$(id -g ${USER}) \
  --build-arg INPUT_GROUP_ID=$(getent group input | cut -d: -f3) \
  -t ${imageName}:latest  \
  ${rootDir}
