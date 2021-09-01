#!/bin/bash

rootDir=$(dirname $0)
rootDir=$(cd ${rootDir}/.. && pwd)
imageName=$(cd ${rootDir} && basename $(pwd))

if [[ -e /dev/input/rfid && -c /dev/input/rfid ]]
then
	docker run -it -p 5000:5000 --mount src=rfid-db,target=/rfid-db --mount src="${rootDir}",target=/rfid-security-svc,type=bind --device=/dev/input/rfid:/dev/input/rfid:r ${imageName}:latest /bin/bash
else
	echo "Did not find /dev/input/rfid, skipping --device"
	docker run -it -p 5000:5000 --mount src=rfid-db,target=/rfid-db --mount src="${rootDir}",target=/rfid-security-svc,type=bind ${imageName}:latest /bin/bash
fi
