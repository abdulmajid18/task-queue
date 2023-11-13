import pika
from celery import Celery

app = Celery(
    'basis-task',
    broker='pyamqp://guest@localhost//',
    backend='rpc://'
)

EXCHANGE_NAME = "data_generation"
QUEUE_NAME = "data_generation_queue"
ROUTING_KEY = "data.generation.topic"


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


@app.task(name="basis.fibonacci_task")
def calculate_fibonacci(n):
    print(f" [.] fib({n})")
    answer = str(fib(n))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='result', exchange_type='topic')
    channel.queue_declare(queue='result_queue', durable=True)
    routing_key = "result.topic"
    channel.queue_bind(exchange='result', queue='result_queue', routing_key=routing_key)
    channel.basic_publish(
        exchange='result', routing_key=routing_key, body=answer.encode("utf-8"))
    print(f" [x] Sent {routing_key}:{answer}")
    connection.close()


def on_request(ch, method, props, body):
    n = int(body)
    calculate_fibonacci(n)


def start_rpc_server():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declare an exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')
    # Declare a queue and bind it to the exchange with a routing key
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)

    channel.basic_qos(prefetch_count=1000)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_request)

    print(" [x] Awaiting RPC requests")
    channel.start_consuming()


if __name__ == '__main__':
    start_rpc_server()
