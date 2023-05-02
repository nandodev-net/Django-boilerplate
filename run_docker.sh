#!/bin/bash
# Use this file to start the production server

if [[ $* == *--build* ]] 
then 
    SHOULD_BUILD="--build" 
else 
    SHOULD_BUILD="" 
fi


if [[ $* == *--dev* ]] 
then 
    DOCKERCOMPOSE_FILE=docker-compose.dev.yml
else 
    DOCKERCOMPOSE_FILE=docker-compose.yml 
fi


printf "Shutting down active servers...\n" &&\
docker compose -f ${DOCKERCOMPOSE_FILE} down &&\
printf "Building docker composer file...\n" &&\
docker compose -f ${DOCKERCOMPOSE_FILE} up -d ${SHOULD_BUILD} &&\
printf "Collecting static files...\n" &&\
docker compose -f ${DOCKERCOMPOSE_FILE} exec web python manage.py collectstatic --no-input --clear &&\
printf "Ready to go!\n" &&\
printf "to run migrations, use the following commnad:\n" &&\
printf "   docker compose -f ${DOCKERCOMPOSE_FILE} exec web python manage.py migrate --noinput\n" &&\
printf "You can test this server by requesting to  http://localhost:1337/admin\n" &&\
printf "Check the logs using: docker compose -f ${DOCKERCOMPOSE_FILE} logs -f\n"                                                                           