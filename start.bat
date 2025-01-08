@echo off
start cmd /k "cd /d C:\Users\User\Documents\Code\Projects\RPA\Portal\server\portal && python manage.py runserver"
start cmd /k "cd /d C:\Users\User\Documents\Code\Projects\RPA\Portal\client && yarn start"
start cmd /k "cd /d C:\Users\User\Documents\Code\Projects\RPA\Portal\server\portal && python manage.py process_tasks"