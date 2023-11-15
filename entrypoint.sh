#!/bin/bash

RABBITMQ_HOST="${RABBITMQ_HOST:-rabbitmq}"
RABBITMQ_PORT="${RABBITMQ_PORT:-5672}"

# Function to check if RabbitMQ is up on port 5672
wait_for_rabbitmq() {
    until nc -z -w 1 "$RABBITMQ_HOST" "$RABBITMQ_PORT"; do
        echo "Waiting for RabbitMQ to be up on $RABBITMQ_HOST:$RABBITMQ_PORT..."
        sleep 10
    done
}

# Call the function to wait for RabbitMQ
wait_for_rabbitmq

# Start your task_listener or any other commands
echo "Starting Task Listener"
python task.py

exec "$@"


