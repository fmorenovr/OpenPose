#!/bin/bash

echo "BUILDING OPENPOSE"
cd /app/openpose/build/python/openpose
cp ./pyopenpose.cpython-36m-x86_64-linux-gnu.so /usr/local/lib/python3.6/dist-packages
cd /usr/local/lib/python3.6/dist-packages
ln -s pyopenpose.cpython-36m-x86_64-linux-gnu.so pyopenpose
export LD_LIBRARY_PATH=/app/openpose/build/python/openpose

echo "DOWNLOADING MODELS"
cd /app/openpose/
rm -rf models/
cd ..
mv models/ /app/openpose/models/
