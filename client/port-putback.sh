#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: put-port.sh <port>"
	exit 0
fi

exec curl -sS "127.0.0.1:5000/putback/$1"
