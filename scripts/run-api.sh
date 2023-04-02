#!/usr/bin/env bash
set -e

if [ -z "$APP_ENV" ]; then
  echo "Please set APP_ENV"
  exit 1
fi

if [ "$APP_ENV" == "local" ]; then
  EXTRA_PARAMS="--reload"
else
  EXTRA_PARAMS=""
fi

exec uvicorn \
    --host $APP_HOST \
    --port $APP_PORT \
    --no-access-log \
    $EXTRA_PARAMS \
    server.main:app
