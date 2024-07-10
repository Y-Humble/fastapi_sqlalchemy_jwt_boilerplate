#!/bin/bash


cd src
alembic upgrade head
gunicorn __main__:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8080
