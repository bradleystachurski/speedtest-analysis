#!/usr/bin/env bash

# copy the raw text file with speedtest results
cp ~/.cronjobs/results.txt $PWD

# source python3.7 from virtualenv
source $PWD/.venv/bin/activate

# parse raw text file and generate data visualization form python script
python main.py

# start express server for generated html
npm run start
