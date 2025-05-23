#!/bin/bash

CONFIG_FILE="src/professional_secure_ai_bot/config.json"

function enable_route() {
    jq '.enable_text_management = true' $CONFIG_FILE > tmp.json && mv tmp.json $CONFIG_FILE
    echo "✅ 已启用 /text-management/submit-text"
}

function disable_route() {
    jq '.enable_text_management = false' $CONFIG_FILE > tmp.json && mv tmp.json $CONFIG_FILE
    echo "❌ 已禁用 /text-management/submit-text"
}

case "$1" in
    enable)
        enable_route
        ;;
    disable)
        disable_route
        ;;
    *)
        echo "Usage: $0 {enable|disable}"
        exit 1
        ;;
esac