
import json
import boto3
import os

from boto3.dynamodb.conditions import Key, Attr
table_name = os.environ.get('TABLE_NAME')


def lambda_handler(event, context):
    print(event)
    body = event["body"]
    print(body)
    body = json.loads(body)
    pk = body['pk']
    sk = body['sk']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.delete_item(
        Key={
            'PK': pk,
            'SK': sk
        }
    )

    header = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Content-Type': 'application/json',
    }
    return{
        'statusCode': 200,
        'headers': header,
        'body': json.dumps({
            'message': 'Deleted single item',

        })
    }
