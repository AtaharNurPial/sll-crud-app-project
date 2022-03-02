
import json
import os
import boto3
import time
# from BaseModel import base_model

client = boto3.client('dynamodb')
# table_name = os.environ.get('TABLE_NAME')

def create_table(table_name):
    response = client.create_table(
        TableName = table_name,
        AttributeDefinitions=[
        {
            'AttributeName': 'PK',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'SK',
            'AttributeType': 'S'
        },
        ],
        KeySchema=[
        {
            'AttributeName': 'PK',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'SK',
            'KeyType': 'RANGE'
        }
        ],
        ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
        }
    )
    return response

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    table_name = body['table_name']
    header = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Content-Type': 'application/json',        
    }
    try:
        menu_item = create_table(table_name)
        time.sleep(5)
        return{
            'statusCode': 200,
            'headers': header,
            'body': json.dumps({
                'error': False,
                'code': 'TABLE_CREATED',
                'message': 'Table created successfully',
                'value': menu_item
            })
        }
    except Exception as e:
        print(e)
        return{
            'statusCode': 400,
            'body': json.dumps({
            'error': True,
            'code': 'UNKNOWN_ERROR',
            'message': 'Some error occured. Please try again.'
            })
        }