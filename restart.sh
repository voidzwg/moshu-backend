#!/bin/bash
killall -9 uwsgi
uwsgi --ini uwsgi.ini
nginx -s reload
python3.8 manage.py runserver 8000