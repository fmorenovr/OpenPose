#!/bin/bash

if [ "$DOWNLOAD_MODELS" == "true" ]; then 
    echo "DOWNLOADING MODELS . . ."
    bash get_models.sh
fi

if [ "$DOWNLOAD_DATA" == "true" ]; then 
    echo "DOWNLOADING DATA . . ."
    bash get_data.sh
fi

if [ "$DEBUG_MODE" == "true" ]; then 
    echo "TESTING"
    python3 -m unittest discover -s ./openpose_test -p test_*.py
fi
