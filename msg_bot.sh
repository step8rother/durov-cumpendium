#!/bin/bash

send_telegram_message() {
    local message=$1
    local TELEGRAM_TOKEN=""
    local TELEGRAM_CHAT_ID=""
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" -d chat_id=${TELEGRAM_CHAT_ID} -d text="${message}"
}

if [ -z "$1" ]; then
    echo "Usage: $0 \"your message here\""
    exit 1
fi

user_msg="$1"

send_telegram_message "${user_msg}"
