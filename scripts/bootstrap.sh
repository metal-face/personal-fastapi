#!/usr/bin/env bash
set -e

if [ -z "$APP_COMPONENT" ]; then
  echo "Please set APP_COMPONENT"
  exit 1
fi

cd /srv/root

/scripts/init-db.sh

# run sql database migrations & seeds
# /scripts/migrate-db.sh up
# /scripts/seed-db.sh up

case $APP_COMPONENT in
  "api")
    exec /scripts/run-api.sh
    ;;

  *)
    echo "'$APP_COMPONENT' is not a known value for APP_COMPONENT"
    ;;
esac