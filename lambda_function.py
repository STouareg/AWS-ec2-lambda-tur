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

regions_bdh = ['us-west-2', 'us-east-1', 'eu-central-1']

instances_bdh = []
instances_bdh.append(['i-011ede8633ccaddf5', 'i-018190af43d573b7c', 'i-00ad8267c4933feb4', 'i-0d4873a4a5c4e9f76'])
instances_bdh.append(['i-05a46d083d39d2fd9', 'i-05c1409696b7e467a', 'i-0abb9d6630d2c7f93'])
instances_bdh.append(['i-01ef855aed2f04059', 'i-02b30b47945cdcd45', 'i-0ee051a5822e33ae1'])

# # -----------------------------------------------------------------------
# region_bdh_usw2 = 'us-west-2'
# region_bdh_use1 = 'us-east-1'
# region_bdh_euc1 = 'eu-central-1'

# instances_bdh_usw2 = ['i-011ede8633ccaddf5', 'i-018190af43d573b7c', 'i-00ad8267c4933feb4', 'i-0d4873a4a5c4e9f76']
# instances_bdh_use1 = ['i-05a46d083d39d2fd9', 'i-05c1409696b7e467a', 'i-0abb9d6630d2c7f93']
# instances_bdh_euc1 = ['i-01ef855aed2f04059', 'i-02b30b47945cdcd45', 'i-0ee051a5822e33ae1']

# ec2_bdh_usw2 =  boto3.client('ec2', region_name=region_bdh_usw2)
# ec2_bdh_use1 =  boto3.client('ec2', region_name=region_bdh_use1)
# ec2_bdh_euc1 =  boto3.client('ec2', region_name=region_bdh_euc1)

# # -----------------------------------------------------------------------

region_transport = 'eu-central-1'
instance_transport = ['i-0d45219704d706da2']
ec2_transport =  boto3.client('ec2', region_name=region_transport)

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
            bot.send_message(chat['id'], 'Transport instance is going to be started.')
            return RESPONSE_200

        elif command == '/Stop_transport_EC2':
            ec2_transport.stop_instances(InstanceIds=instance_transport)
            bot.send_message(chat['id'], 'Transport instance is going to be stopped.')
            return RESPONSE_200

                                 
        elif command == '/Start_BDH_EC2':
            count = 0

            # for i in range(len(regions_bdh)):
            #     ec2_bdh = boto3.client('ec2', region_name=regions_bdh[i])
            #     bot.send_message(chat['id'], regions_bdh[i])
            #     for j in range(len(instances_bdh[i])):
            #         instance = [instances_bdh[i][j]]
            #         bot.send_message(chat['id'], instance)
            #         response = ec2_bdh.start_instances(InstanceIds=[instance,])
            #         bot.send_message(chat['id'], response.StartingInstances.InstanceId)
            #         return RESPONSE_200
                              
            return RESPONSE_200

        elif command == '/Stop_BDH_EC2':
            # count = 0
            # while count < len(regions_bdh):
            #     instance = []
            #     ec2_bdh = boto3.client('ec2', region_name=regions_bdh[count])
            #     for i in range (0,len(instances_bdh[count])):
            #         instance.append(instances_bdh[count][i])
            #         ec2_bdh.stop_instances(InstanceIds=instance)
            #         string_instance = 'The instance ' + instances_bdh[count][i] + ' stopped.'
            #         bot.send_message(chat['id'], string_instance)
            #     count += 1
            return RESPONSE_200

        # elif command == '/BDH_EC2_status':
        #     for instance in instances_bdh_usw2:
        #         # instance_list = [instance]
        #         bdh_usw2_status = ec2_bdh_usw2.describe_instance_status(InstanceIds=instance)
        #         # bdh_use1_status = ec2_bdh_use1.describe_instance_status(InstanceIds=instances_bdh_use1)
        #         # bdh_euc1_status = ec2_bdh_euc1.describe_instance_status(InstanceIds=instances_bdh_euc1)
        #         # if bdh_usw2_status['InstanceStatuses'][0]['InstanceState']['Name'] == 'running':
        #         #     print('It is running')
        #         bot.send_message(chat['id'], bdh_usw2_status['InstanceStatuses'][instances_bdh_usw2.index(instance)]['InstanceId'])
        #         bot.send_message(chat['id'], bdh_usw2_status['InstanceStatuses'][instances_bdh_usw2.index(instance)]['InstanceState']['Name'])
        #         # bot.send_message(chat['id'], bdh_use1_status)
        #         # bot.send_message(chat['id'], bdh_euc1_status)
        #     return RESPONSE_200


        elif command == '/GetCurrentMonthlyCost':
            client = boto3.client('ce')
            todayDate  = datetime.date.today()
            first_day_of_month = todayDate.replace(day=1)
            billing = client.get_cost_and_usage(
                TimePeriod={
                    "Start": str(first_day_of_month),
                    "End": str(todayDate)},
                Granularity = 'MONTHLY',
                Metrics = ["UnblendedCost",]
            )
            for r in billing['ResultsByTime']:
                str_amount=(r['Total']['UnblendedCost']['Amount'])

            str_amount = str_amount[:5] + ' usd'
            bot.send_message(chat['id'], str_amount)
            return RESPONSE_200

        elif command == '/GetCurrentMonthlyForecast':
            client = boto3.client('ce')
            todayDate  = datetime.date.today()
            last_day_of_month = (todayDate.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

            forecast = client.get_cost_forecast(
                TimePeriod={
                    "Start": str(todayDate),
                    "End": str(last_day_of_month)},
                Metric = 'UNBLENDED_COST',
                #Granularity = 'DAILY'
                Granularity = 'MONTHLY'
            )
            forecast = forecast['Total']['Amount'][:5] + ' usd'
            bot.send_message(chat['id'], forecast)
            return RESPONSE_200

        elif command == '/help':
            bot.send_message(chat['id'], 'You can type this:\n\
/Start_transport_EC2,\n/Stop_transport_EC2,\n\
/Start_BDH_EC2,\n/Stop_BDH_EC2,\n\
/BDH_EC2_status,\n\
/GetCurrentMonthlyCost,\n/GetCurrentMonthlyForecast,\n\n\
/help')
            return RESPONSE_200

        else:
            bot.send_message(chat['id'], "Hello. You can type /help to release help docs.")
            return RESPONSE_200

    else:
        bot.send_message(chat['id'], "You not allowed.")
        return RESPONSE_200

    return RESPONSE_200
