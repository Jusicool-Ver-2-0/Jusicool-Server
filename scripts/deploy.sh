#!/bin/bash


if [[ "$DEPLOYMENT_GROUP_NAME" == "stage" ]]; then
  /home/ubuntu/stage/Jusicool-Server/scripts/stage.sh
elif [[ "$DEPLOYMENT_GROUP_NAME" == "prod" ]]; then
  /home/ubuntu/prod/Jusicool-Server/scripts/prod.sh
fi