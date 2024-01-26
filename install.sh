#!/bin/bash

mkdir application
cp run.sh plot.py application

chmod +x application/run.sh
#export PYTHONPATH="${PYTHONPATH}:${PWD}/application"
#export PATH="${PATH}:${PWD}/application"