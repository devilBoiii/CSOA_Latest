#!/bin/bash

# Start MySQL
# Copy the dump file into the container
docker cp csoa_database_dump.sql mysql_csoa:/csoa_database_dump.sql

# Run the MySQL command to import the dump
docker exec -i mysql_csoa mysql -u root -p'root' csoa_database < /csoa_database_dump.sql

# Clean up the dump file from the container
docker exec -it mysql_csoa rm /csoa_database_dump.sql


# Run docker-compose down
docker-compose down
docker-compose up -d --build
