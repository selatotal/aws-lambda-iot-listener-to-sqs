import time
import boto3
import uuid
import os
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def callback(client, userdata, message):
    sqs = boto3.resource("sqs")
    queue = sqs.get_queue_by_name(QueueName=os.environ.get('SQS_QUEUE'))
    queue.send_message(
        MessageBody = str(message.payload),
        MessageDeduplicationId = str(uuid.uuid4()),
        MessageGroupId = "lambdaApp")


def handler(event, context):
    mqttClient = AWSIoTMQTTClient("lambdaApp", cleanSession=False)
    mqttClient.configureEndpoint(os.environ.get('IOT_ENDPOINT'), 443)
    mqttClient.configureConnectDisconnectTimeout(10)
    mqttClient.configureCredentials(os.environ.get('CA_FILE_PATH'), os.environ.get('CERT_KEY_PATH'), os.environ.get('CA_FILE_PATH'))
    mqttClient.configureMQTTOperationTimeout(10)
    mqttClient.connect()
    mqttClient.subscribe(os.environ.get('IOT_TOPIC'), 1, callback)
    time.sleep(30)
    mqttClient.disconnect()
    return {
        "message": "Messages received",
    }

if __name__ == "__main__":
    handler("test", "test")
