#!/bin/bash

rootDir=$(dirname $0)
rootDir=$(cd ${rootDir}/.. && pwd)
imageName=$(cd ${rootDir} && basename $(pwd))

docker run -p 5000:5000 --mount src=rfid-db,target=/rfid-db ${imageName}:production $@
