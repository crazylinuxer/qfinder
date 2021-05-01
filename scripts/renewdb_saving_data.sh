#!/bin/bash

export start_pwd=$PWD
while [[ $PWD == *"scripts"* ]]; do
    cd ..
done

source ./scripts/auxiliary/prepare_launch.sh

if [[ $PGPASSWORD != '' ]]; then
    pg_dump -Fc -Z0 --data-only -U qfinder_user qfinder_db > ./qfinder_db_data.pgdump

    dropdb -U qfinder_user qfinder_db
    createdb -U qfinder_user qfinder_db
    psql qfinder_db -U qfinder_user < ./sql/qfinder_db.sql

    pg_restore -U qfinder_user --data-only -d qfinder_db ./sql/qfinder_db_data.pgdump
    rm -f ./qfinder_db_data.pgdump
fi

cd $start_pwd
