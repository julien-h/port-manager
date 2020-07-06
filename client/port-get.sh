#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage get-port.sh 'name'"
	exit 0
fi

exec curl -sS "127.0.0.1:5000/get/$1"
