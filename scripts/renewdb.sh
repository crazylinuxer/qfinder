#!/bin/bash

export start_pwd=$PWD
while [[ $PWD == *"scripts"* ]]; do
    cd ..
done

source ./scripts/auxiliary/prepare_launch.sh

if $(password_check); then
    dropdb -U qfinder_user qfinder_db
    createdb -U qfinder_user qfinder_db
    psql qfinder_db -U qfinder_user < ./sql/qfinder_db.sql
    pg_restore -U qfinder_user --data-only --disable-triggers -d qfinder_db ./sql/data.pgdump
fi

cd $start_pwd
