#!/usr/bin/env bash

python manage.py init_groups

python manage.py create_team
python manage.py create_projects
python manage.py create_buys --add
python manage.py create_content
