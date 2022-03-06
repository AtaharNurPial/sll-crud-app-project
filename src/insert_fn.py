import boto3
import os, json
from pydantic import ValidationError
from BaseModel import base_model

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def insert_into(menu_item):
    table_response = table.put_item(
        TableName = table_name,
        Item=menu_item.dict(),
        # ConditionExpression = 'attribute_not_exists(menu_item.PK) & attribute_not_exists(menu_item.SK)'
    )
    print(table_response)
    return table_response

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    menu_item = base_model.Menu_Item(**body)
    header = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*',
    }
    # print(type(body))
    try:
        response = insert_into(menu_item)
        return{
            'statusCode': 200,
            'headers': header,
            'body': json.dumps({
                'error': False,
                'code': 'ITEM_INSERTED',
                'message': 'Item inserted Successfully',
                'value': menu_item.dict()
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
        return{
            'statusCode': 400,
            'headers': header,
            'body': json.dumps({
                'error': True,
                'code': 'RESOURCE_NOT_FOUND',
                'message': 'Table does not exist or resource could not be found. Please try again'
            })
        }