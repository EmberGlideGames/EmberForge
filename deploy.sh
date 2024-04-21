#!/bin/bash

source /home/loran425/emberglide/venv/bin/activate

rm -rf /var/www/emberglide/*

blag build

cp -r ./build/* /var/www/emberglide

rm -rf ./build/*
