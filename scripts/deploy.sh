#!/bin/bash


if [[ "$DEPLOYMENT_GROUP_NAME" == "stage" ]]; then
  /ubuntu/home/stage/Jusicool-Server/scripts/stage.sh
elif [[ "$DEPLOYMENT_GROUP_NAME" == "prod" ]]
  /ubuntu/home/prod/Jusicool-Server/scripts/prod.sh
fi