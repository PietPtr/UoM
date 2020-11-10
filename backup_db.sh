#!/bin/bash


if [ -z "$1" ]
then
    echo "Please supply a file to write the backup to."
else
    pg_dump -d uom -f $1
fi
