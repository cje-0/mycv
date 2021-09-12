#!/bin/sh

DOCKER="/usr/bin/podman"
${DOCKER} build -t mycv:latest .
