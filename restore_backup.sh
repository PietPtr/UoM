#!/bin/bash


if [ -z "$1" ]
then
    echo "Please supply a file to restore the backup from."
else
    read -p "Are you sure? This will delete the current database and restore to \`$1' " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "Restoring backup from $1..."
        set -e
        dropdb uom
        createdb uom
        psql -d uom -f $1
    fi
fi

