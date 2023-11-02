
# uptime_info=$(uptime)

# echo "System uptime: $uptime_info"


#!/bin/bash

log_file="/var/log/monthly_uptime.log"

# Get the current date
current_date=$(date "+%Y-%m-%d")

# Get the system uptime
uptime_info=$(uptime)

# Append the uptime information to the log file
echo "$current_date: $uptime_info" >> "$log_file"

# Display the current uptime
echo "System uptime on $current_date: $uptime_info"
