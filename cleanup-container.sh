#!/bin/sh

DOCKER="/usr/bin/podman"
${DOCKER} container prune -f
${DOCKER} image prune -f
