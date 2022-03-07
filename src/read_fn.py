import json
import boto3
import os
from pydantic import ValidationError

from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def read_item(pk,sk):
    table_response = table.get_item(
        TableName = table_name,
        Key={
            'PK': pk,
            'SK': sk
        }
    ) 
    print(table_response)
    return table_response


def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    pk = body['pk']
    sk = body['sk']
    header = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*',
    }
    try:
        response = read_item(pk,sk)
        item = response['Item']
        print(item)
        return{
            'statusCode': 200,
            'headers': header,
            'body': json.dumps({
                'error': False,
                'code': 'ITEM_READ',
                'message': 'single item',
                "item": item
            })
        }
    except ValidationError as e:
        return{
            'statusCode': 400,
            'headers': header,
            'body': json.dumps({
                'error': True,
                'code': 'VALIDATION_ERROR',
                'message': str(e)
            })
        }
    except table.exceptions.ResourceNotFoundException as e:
        print(e)
        return {
            'statusCode': 400,
            'headers': header,
            'body': json.dumps({
            'error': True,
            'code': 'RESOURCE_NOT_FOUND',
            'message': 'The table is not valid or the resource is not specifiend correctly.Please try again.'
            })
        }