#!/bin/bash

export FLASK_APP=rfidsecuritysvc
export FLASK_ENV=development

flask "$@"
