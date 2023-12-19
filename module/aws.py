import boto3
import json
from configparser import ConfigParser


class SQS:
    def __init__(self):
        config = ConfigParser()
        config.read('./config/config.ini')
        config = config['sqs']

        sqs = boto3.resource('sqs',
                             region_name=config['region'],
                             endpoint_url=config['endpoint_url'],
                             aws_access_key_id=config['aws_access_key_id'],
                             aws_secret_access_key=config['aws_secret_access_key']
                             )
        self.queue = sqs.get_queue_by_name(QueueName='test1')

    def consume(self):
        return self.queue.receive_messages(MaxNumberOfMessages=1)

    def produce(self, message):
        return self.queue.send_message(MessageBody=json.dumps(message))


