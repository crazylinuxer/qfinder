#!/bin/bash

export start_pwd=$PWD
while [[ $PWD == *"scripts"* ]]; do
    cd ..
done

source ./scripts/auxiliary/prepare_launch.sh

if $(password_check); then
    pg_dump -U qfinder_user --schema-only qfinder_db > ./sql/qfinder_db.sql
    pg_dump -Fc -Z0 -U qfinder_user --data-only qfinder_db > ./sql/data.pgdump
fi

cd $start_pwd
