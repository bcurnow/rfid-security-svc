#!/bin/bash

currentDir=$(dirname $0)
currentDir=$(cd ${currentDir} && basename $(pwd))

docker run -it -p 5000:5000 --mount src="$(pwd)",target=/${currentDir},type=bind ${currentDir}:latest /bin/bash
