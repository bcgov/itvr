#!/bin/bash
python worker_hc.py &
python manage.py qcluster
