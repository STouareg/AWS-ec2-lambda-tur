import telebot
import boto3
import os
import datetime
import json

RESPONSE_200 = {
      "statusCode" : 200,
      "headers"    : {},
      "body"       : ""
    }

# region_usw2 = 'us-west-2'
# region_use1 = 'us-east-1'
# region_euc1 = 'eu-central-1'
regions_bdh = ['us-west-2', 'us-east-1', 'eu-central-1']

# instances[0] = ['i-011ede8633ccaddf5', 'i-018190af43d573b7c', 'i-00ad8267c4933feb4', 'i-0d4873a4a5c4e9f76']
# instances[1] = ['i-05a46d083d39d2fd9', 'i-05c1409696b7e467a', 'i-0abb9d6630d2c7f93']
# instances[2] = ['i-01ef855aed2f04059', 'i-02b30b47945cdcd45', 'i-0ee051a5822e33ae1']


region_transport = 'us-west-2'
instance_transport = ['i-011ede8633ccaddf5'] #DELIKSPLUS-Wireguard

# region_transport = 'eu-central-1'
# instance_transport = ['i-0d45219704d706da2'] #real transport

# for N in len(regions_bdh):
#     ec2_bdh[N] = boto3.client('ec2', region_name=regions_bdh[N])

ec2_transport =  boto3.client('ec2', region_name=region_transport)

# ec2_usw2 = boto3.client('ec2', region_name=region_usw2)
# ec2_use1 = boto3.client('ec2', region_name=region_use1)
# ec2_euc1 = boto3.client('ec2', region_name=region_euc1)

# ec2_usw2.start_instances(InstanceIds=instances_usw2)
# ec2_use1.start_instances(InstanceIds=instances_use1)
# ec2_euc1.start_instances(InstanceIds=instances_euc1)


def lambda_handler(event, context):
    update = telebot.types.JsonDeserializable.check_json(event["body"])
    TOKEN     = os.environ['BOT_TOKEN']
    ADMINCHAT = os.environ['ADMIN']

    message = update.get('message')
    if not message:
        return RESPONSE_200

    chat = message.get('chat')
    bot = telebot.TeleBot(TOKEN)

    command = message.get('text', '')
    if chat['id'] == int(ADMINCHAT):

        if command == '/Start_transport_EC2':
            ec2_transport.start_instances(InstanceIds=instance_transport)
            return RESPONSE_200

        elif command == '/Stop_transport_EC2':
            ec2_transport.stop_instances(InstanceIds=instance_transport)
            return RESPONSE_200

        elif command == '/help':
            bot.send_message(chat['id'], 'You can type this: /Start_transport_EC2, /Stop_transport_EC2, /GetCurrentMonthlyCost, /GetCurrentMonthlyForecast, /help')
            return RESPONSE_200

        else:
            bot.send_message(chat['id'], "Hello. You can type /help to release help docs.")
            return RESPONSE_200

    else:
        bot.send_message(chat['id'], "You not allowed.")
        return RESPONSE_200

    return RESPONSE_200
