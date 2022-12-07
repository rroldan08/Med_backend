#!/bin/bash
tmux kill-session -t portfolio_session
cd project
source env/bin/activate
cd med_tracker
python manage.py runserver 0.0.0.0:8000
