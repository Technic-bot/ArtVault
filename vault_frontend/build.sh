#!/usr/bin/env bash
#./deploy usuario servidor /home/path/to/deploy

USER=$1
SERVER=$2
URI=$3

npm run build
rm vault.zip
zip -r vault.zip build/

scp_location="$USER@$SERVER:$URI"
echo "Copying vault.zip to "
scp vault.zip "$scp_location"

