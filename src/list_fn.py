
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
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key('PK').eq(pk)
    )

    items = response['Items']
    print(items)
    header = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Content-Type': 'application/json',
    }
    return{
        'statusCode': 200,
        'headers': header,
        'body': json.dumps({
            'message': 'List of all Items',
            "list": items
        })
    }
