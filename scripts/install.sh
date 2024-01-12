#!/bin/bash

# Define the base directory of the repository
BASE_DIR="$(dirname "$(dirname "$(realpath "$0")")")"
BIN_DIR="${BASE_DIR}/src/terminalmind_bin"

# Copying scripts and configuration file to /usr/local/bin
echo "Installing terminalmind..."

# Check if /usr/local/bin is writable
if [ ! -w "/usr/local/bin" ]; then
    echo "Error: /usr/local/bin is not writable. Try running with elevated permissions."
    exit 1
fi

# Copy the contents of terminalmind_bin to /usr/local/bin
cp -r "${BIN_DIR}/"*.py /usr/local/bin/
cp "${BIN_DIR}/terminalmind" /usr/local/bin/
cp "${BIN_DIR}/terminalmindcore" /usr/local/bin/
cp "${BIN_DIR}/config.sh" /usr/local/bin/

# Ensure all scripts and the config file are executable
chmod +x /usr/local/bin/*.py
chmod +x /usr/local/bin/terminalmind
chmod +x /usr/local/bin/terminalmindcore
chmod +x /usr/local/bin/config.sh

# Source the config.sh file to verify the model path
source /usr/local/bin/config.sh

if [ ! -f "$MODEL_PATH" ]; then
    echo "Warning: Model file not found at $MODEL_PATH. Please update /usr/local/bin/config.sh with the correct model path."
else
    echo "Model path set to $MODEL_PATH."
fi

echo "terminalmind installed successfully."
