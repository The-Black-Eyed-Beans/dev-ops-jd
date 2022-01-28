#!/bin/bash
echo "Executing python script..."
MYSQL_HOST=172.24.233.32 \
MYSQL_PORT=30201 \
MYSQL_USER=root \
MYSQL_PASSWORD=123456 \
MYSQL_DATABASE=alinedb \
USER_ROLE=admin \
USER_USERNAME=blackEyeBeans \
USER_PASSWORD=Abc123456* \
USER_FIRSTNAME=Izuku \
USER_LASTNAME=Midoriya \
USER_EMAIL=deku@gmail.com \
USER_PHONE=864-324-4568 \
BASE_URL=172.24.233.32:30200 \
python index.py
echo "Execution completd!"