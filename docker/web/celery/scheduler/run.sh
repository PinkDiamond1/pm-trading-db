#!/bin/bash

set -euo pipefail

# DEBUG set in .env_docker_compose
if [ ${DEBUG:-0} = 1 ]; then
    log_level="debug"
else
    log_level="info"
fi

sleep 5
echo "==> Running Celery beat <=="
exec celery beat -A tradingdb.taskapp -S django_celery_beat.schedulers:DatabaseScheduler --loglevel $log_level
