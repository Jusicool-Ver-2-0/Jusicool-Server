#!/bin/sh

mkdir -p /home/ubuntu/prod/Jusicool-Server

cd /home/ubuntu/prod/Jusicool-Server

if [ ! -d ".git" ]; then
  git clone -b main https://github.com/bigbroCO-team/bigbro_company_server .
else
  git pull origin main
fi

docker build . -t jusicool-prod

docker stop jusicool-prod  || true
docker rm jusicool-prod || true

docker run -d --name jusicool-prod --env-file /.prod.env -p 3000:8000 jusicool-prod