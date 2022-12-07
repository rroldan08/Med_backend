#!/bin/bash
source env/bin/activate
cd proyecto_musica
python manage.py runserver 0.0.0.0:8000
