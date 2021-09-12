#!/bin/sh

DOCKER="/usr/bin/podman"
# ${DOCKER} run --rm -a=stdout -a=stderr -v ./src:/code:Z mycv:latest python /code/cv.py 1
${DOCKER} run --rm -a=stdout -a=stderr -v ./src:/code:Z -v ./example-data:/code/data:Z mycv:latest python /code/cv.py 1
