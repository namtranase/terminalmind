#!/bin/bash

# Define the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Path to the configuration directory and default configuration file
CONFIG_DIR="$HOME/.config/temi"
CONFIG_FILE="$CONFIG_DIR/temi_config.json"

# Ensure jq is installed
if ! command -v jq &>/dev/null; then
    echo "jq is not installed. Please install jq to use this script."
    exit 1
fi

# Function to load the configuration from the JSON file
load_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        # Provide a default configuration if the config file is missing
        mkdir -p "$CONFIG_DIR"
        echo '{"model_path": "~/llm_models/model.gguf", "type": "local"}' > "$CONFIG_FILE"
        echo "Default configuration created at '$CONFIG_FILE'."
    fi

    MODEL_PATH=$(jq -r '.model_path' "$CONFIG_FILE")
    MODEL_TYPE=$(jq -r '.type' "$CONFIG_FILE")

    # Resolve tilde and parameter expansion
    MODEL_PATH=$(eval echo "$MODEL_PATH")

    # Check if the model path is valid
    if [ "$MODEL_TYPE" == "local" ] && [ ! -f "$MODEL_PATH" ]; then
        echo "Invalid model path in configuration: '$MODEL_PATH'"
    fi
}

# Function to update the configuration file
update_config() {
    local new_config_path="$1"

    if [ ! -f "$new_config_path" ]; then
        echo "The provided configuration file does not exist: '$new_config_path'"
        exit 1
    fi

    # Copy the new configuration file to the standard location
    cp "$new_config_path" "$CONFIG_FILE"
    echo "Configuration updated successfully."

    # Reload the configuration
    load_config
}

# Check if the user wants to update the configuration
if [[ "$1" == "update_config" ]]; then
    update_config "$2"
    exit 0
fi

# Load configuration settings
load_config
