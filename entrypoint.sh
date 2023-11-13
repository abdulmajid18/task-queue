#!/bin/bash

echo "Waiting for RabbitMQ..."

while ! nc -z -w 1 "rabbitmq" "5672"; do
    sleep 20
done

echo "RabbitMQ started"


echo "Starting worker"
python task.py

exec "$@"

