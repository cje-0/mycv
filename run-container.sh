#!/bin/sh

DOCKER="/usr/bin/podman"
${DOCKER} run --rm -a=stdout -a=stderr -v ./src:/code:Z -v ./data:/code/data:Z -v ./output:/code/output:Z mycv:latest python /code/cv.py "$@"
