import pika
import time
import dbds
import sys

if __name__ == "__main__":
    host_ip = sys.argv[1]
    connection= pika.BlockingConnection(
                pika.ConnectionParameters(host=host_ip))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_qos(prefetch_count=1)

    def callback(ch, method, properties, body):
        db_response = dbds.insert_db(body.decode(),host_ip)
        print(" [x] Received %r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    channel.start_consuming()



