#!/bin/bash
cd ../backend/
python3 -m venv .venv
source .venv/bin/activate
python3 --version
python3 -m pip install -r requirements.txt
make db-upgrade
make run
