#!/bin/bash
set -e
cd /home/app-user
pm2 start app.config.js --name "sample-app"
pm2 save
