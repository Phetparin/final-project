#This code to publish the data to rabbitmq
#This code is used by flaskapp.py

import sys
import pika

def publisher(message, host_ip):
    connection= pika.BlockingConnection(
            pika.ConnectionParameters(host=host_ip))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    
    channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2, # make message persistent
            ))
    
    print(" [x] Sent %r" % message)
    connection.close()
    return "ok"

if __name__ == '__main__':
    if sys.argv[1:] is None:
        host_ip = "mongodb://localhost:27017/"
    else:
        host_ip = "mongodb://"+sys.argv[1]+":27017/"
    message = "test"
    publisher(message, sys.argv[1])


