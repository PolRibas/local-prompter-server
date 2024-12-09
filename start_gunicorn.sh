#!/bin/bash

# Activar el entorno virtual
source /home/grizzly/Documents/domains/grizzly-server/venv/bin/activate

# Iniciar Gunicorn en segundo plano
nohup gunicorn grizzly_server.wsgi:application --bind 0.0.0.0:8000 --workers 3 &

# Opcional: Guardar el PID para futuros usos
echo $! > /home/grizzly/Documents/domains/grizzly-server/gunicorn.pid
