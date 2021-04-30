#!/bin/bash


while [[ $PWD == *"scripts"* ]]; do
    cd ..
done

export PGPASSWORD='qual1tyf1nder'
export JWT_KEY=$(cat ./scripts/encrypted_vars/jwt)
