#!/bin/bash


if [[ "$DEPLOYMENT_GROUP_NAME" == "stage" ]]; then
  chmod +x /home/ubuntu/stage/Jusicool-Server/scripts/stage.sh
  /home/ubuntu/stage/Jusicool-Server/scripts/stage.sh
elif [[ "$DEPLOYMENT_GROUP_NAME" == "prod" ]]; then
  chmod +x /home/ubuntu/prod/Jusicool-Server/scripts/prod.sh
  /home/ubuntu/prod/Jusicool-Server/scripts/prod.sh
fi