#!/bin/sh

sleep 15
celery -A proj worker -l info