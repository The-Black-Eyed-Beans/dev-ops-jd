~~db-injector ~~
This is a friendly python script to populate our given database "alinedb" with data. 
In order to run you must pass the following environment variables
About 100 records of each table will be created. This can be easliy adjusted in index.py @ 13.
Each run will produce a log file. Remember to clean up (-:
**dockerfile @ joshuad23/aline-db-injector:2.0

env.
- MYSQL_HOST=<STRING>
- MYSQL_PORT=<INT>
- MYSQL_USER=<STRING>
- MYSQL_PASSWORD=<INT>
- MYSQL_DATABASE=<STRING>
- USER_ROLE=<STRING>
- USER_USERNAME=<STRING>
- USER_PASSWORD=<STRING>
- USER_FIRSTNAME=<STRING>
- USER_LASTNAME=<STRING>
- USER_EMAIL=<STRING>
- USER_PHONE=<STRING>
- BASE_URL=<STRING>

ex.
- MYSQL_HOST="localhost"
- MYSQL_PORT=3306 
- MYSQL_USER="root"
- MYSQL_PASSWORD=123456 
- MYSQL_DATABASE="alinedb"
- USER_ROLE="admin"
- USER_USERNAME="blackEyeBeans"
- USER_PASSWORD="Abc123456*"
- USER_FIRSTNAME="Izuku"
- USER_LASTNAME="Midoriya"
- USER_EMAIL="deku@gmail.com"
- USER_PHONE="864-324-4568"
- BASE_URL="localhost:8073"

created @12/17/2021
updated @ 1/27/2022
