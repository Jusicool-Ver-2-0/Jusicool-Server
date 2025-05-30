#!/bin/sh

mkdir -p /home/ubuntu/stage/Jusicool-Server

cd /home/ubuntu/stage/Jusicool-Server

if [ ! -d ".git" ]; then
  git clone -b develop https://github.com/Jusicool-Ver-2-0/Jusicool-Server .
else
  git pull origin develop
fi

docker-compoes up -d --build

docker system prune -f