#!/bin/sh

mkdir -p /home/ubuntu/prod/Jusicool-Server

cd /home/ubuntu/prod/Jusicool-Server

if [ ! -d ".git" ]; then
  git clone -b main https://github.com/Jusicool-Ver-2-0/Jusicool-Server .
else
  git pull origin main
fi

docker-compose up -d --build

docker system prune -f