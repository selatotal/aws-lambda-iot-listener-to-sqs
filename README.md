# aws-lambda-iot-listener-to-sqs
Lambda Function to read a MQTT topic and publish messages in a FIFO queue in SQS

# The Problem
* Need to warantee order to process MQTT messages
* AWS IoT Rules does not support SQS FIFO Queues. Because the Rules Engine is a fully distributed service, there is no guarantee of message order when the SQS action is triggered. (https://docs.aws.amazon.com/iot/latest/developerguide/iot-rule-actions.html#sqs-rule)
* The same occurs with Lambda functions triggered by AWS IoT Rules Engine, because Lambda functions are executed asynchronously. (https://docs.aws.amazon.com/iot/latest/developerguide/iot-rule-actions.html#lambda-rule).
* boto3 API doesn't have methods to subscribe a MQTT topic

# The Solution
* Create a Lambda function that can be triggered by a AWS Cloudwatch Event Schedule to get messages from MQTT and publish in a FIFO Queue.
* Need to use aws-iot-device-sdk-python, that doesn't have native support in AWS Lambda runtime environment

# Serverless Framework
In order to create Lambda Application, I used the Serverless Framework.
According its documentation, "The Serverless Framework consists of an open source CLI that makes it easy to develop, deploy and test serverless apps across different cloud providers, as well as a hosted Dashboard that includes features designed to further simplify serverless development, deployment, and testing, and enable you to easily secure and monitor your serverless apps."

# Deploying with serverless

1 - Install serverless CLI using NPM (https://serverless.com/framework/docs/getting-started/)
```bash
npm install -g serverless
``` 

2 - Access application path and install required serverless plugins
```bash
cd mqtt-to-sqs
serverless plugin install -n serverless-python-requirements
```

3 - Configure AWS Credentials to use
```bash
serverless config credentials --provider aws --key YOUR_AWS_ACCESS_KEY_ID --secret YOUR_AWS_SECRET_ACCESS_KEY
```

4 - Configure Application (see next session)

5 - Deploy application in AWS
```bash
serverless deploy
```

# Configure Application

In order to deploy this Lambda Application in AWS, you need to configure [serverless.yml](mqtt-to-sqs/serverless.yml) file, fixing the following keys:
* IOT-ENDPOINT: Endpoint that allows you to connect to AWS IoT. You can get it in IoT AWS Console, in "Settings" session.
* IOT-TOPIC: MQTT Topic that Lambda should subscribe. You can use MQTT topic Wildcards to do that.
* SQS-QUEUE: SQS Queue name used to receive the messages

As the application will connect in your MQTT server, you need to include your certificate in "certs" folder and configure CA_FILE_PATH and CERT_KEY_PATH in serverless.yml. 
The certificate should be configured in AWS IoT Core Console, in "Secure" session

* The application is using by default "us-east-1" region. You can change it in serverless.yml

# To know more:
* [AWS IoT Rule Actions - SQS Rule](https://docs.aws.amazon.com/iot/latest/developerguide/iot-rule-actions.html#sqs-rule)
* [AWS IoT Rule Actions - Lambda Rule](https://docs.aws.amazon.com/iot/latest/developerguide/iot-rule-actions.html#lambda-rule)
* [Serverless Framework](https://serverless.com)
* [AWS IoT Device SDK for Python](https://github.com/aws/aws-iot-device-sdk-python)
