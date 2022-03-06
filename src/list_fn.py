import os, json
import boto3
from pydantic import ValidationError
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def list_item(pk):
    table_response = table.query(
        TableName = table_name,
        KeyConditionExpression=Key('PK').eq(pk)
    )
    print(table_response)
    return table_response

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    pk = body['pk']
    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table(table_name)
    # response = table.query(
    #     KeyConditionExpression=Key('PK').eq(pk)
    # )
    header = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Content-Type': 'application/json',
    }
    try:
        response = list_item(pk)
        items = response['Items']
        print(items)
        return{
            'statusCode': 200,
            'headers': header,
            'body': json.dumps({
                'error': False,
                'code': 'LIST_SUCCESSFULL',
                'message': 'List of all Items',
                "list": items
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
    except table.exceptions.ConditionalCheckFailedException as e:
        print(e)
        return{
            'statusCode': 400,
            'headers': header,
            'body': json.dumps({
                'error': True,
                'code': 'CONDITIONAL_CHECK_FAILED',
                'message': 'Conditional check did not match.',
            })
        }
    except table.exceptions.ResourceNotFoundException as e:
        print(e)
        return{
            'statusCode': 400,
            'headers': header,
            'body': json.dumps({
                'error': True,
                'code': 'RESURCE_NOT_FOUND',
                'message': 'Resource could not be found.',
            })
        }

