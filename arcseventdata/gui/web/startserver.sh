#!/usr/bin/env bash

cd drchops/bin/
./journald.py
./idd.py
cd -
./SimpleHttpServer.py

