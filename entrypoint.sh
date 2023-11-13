#!/bin/bash

# Function to check if RabbitMQ is up on port 5672
wait_for_rabbitmq() {
    until nc -z -w 1 "rabbitmq" "5672"; do
        echo "Waiting for RabbitMQ to be up..."
        sleep 20
    done
}

# Call the function to wait for RabbitMQ
wait_for_rabbitmq

# Start your task_listener or any other commands
echo "Starting Task Listener"
python task.py

exec "$@"


