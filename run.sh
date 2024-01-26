#!/bin/bash

wget https://raw.githubusercontent.com/MilenaValentini/TRM_Dati/main/Nemo_6670.dat -P application

cd application
python3 plot.py Nemo_6670.dat
