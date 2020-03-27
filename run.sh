#!/bin/bash

PLATFORM=$1

echo "Running '$PLATFORM'"
cd ./$PLATFORM/
docker-compose build && docker-compose up