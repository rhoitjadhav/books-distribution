#!/bin/bash

set -e

# Install pydevd-pycharm
pip install --root-user-action=ignore pydevd-pycharm~=241.14494.241 > /dev/null &

# Start FastAPI server
watchmedo auto-restart --pattern="*.py" --recursive -- uvicorn main:app --host 0.0.0.0 --port 8545
