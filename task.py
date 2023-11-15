import pika
import multiprocessing
import os

print("RPC SERVER INITIALIZED")

EXCHANGE_NAME = "generation_exchange"
QUEUE_NAME = "generation_queue"
ROUTING_KEY = "generation_route"

rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
rabbitmq_port = os.environ.get('RABBITMQ_PORT', '5672')


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def calculate_fibonacci(n):
    print(f" [.] fib({n})")
    return str(fib(n))


def on_request(ch, method, props, body):
    n = int(body)
    print(f"Received this {n}")
    response = calculate_fibonacci(n)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)



def worker():     
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
    channel = connection.channel()
    # Declare an exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct', durable=True)

    # Declare a queue and bind it to the exchange with a routing key
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)

    channel.basic_qos(prefetch_count=1000)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_request)
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()


def start_rpc_server():
    # Create multiple worker processes to handle requests concurrently
    num_processes = 6  # You can adjust this based on your server's capacity
    processes = []

    for _ in range(num_processes):
        process = multiprocessing.Process(target=worker)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    start_rpc_server()


#
# def on_request(ch, method, props, body):
#     print("Task Received Processing")
#     n = int(body)
#     print(f"Received this {n}")
#     task_id = calculate_fibonacci.delay(n)
#     response = {'task_id': str(task_id), 'status': 'processing'}
#     print(response)
#     return response
#
#
# def start_rpc_server():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#     channel = connection.channel()
#
#     # Declare an exchange
#     channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')
#
#     # Declare a queue and bind it to the exchange with a routing key
#     channel.queue_declare(queue=QUEUE_NAME, durable=True, exclusive=False)
#     channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)
#
#     channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_request, auto_ack=True)
#
#     print(" [x] Awaiting RPC requests")
#     channel.start_consuming()

#
# if __name__ == '__main__':
#     start_rpc_server()
