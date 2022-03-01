
import json

def lambda_handler(event, context):
    print(event)
    return{
        'statusCode': 200,
        'headers': {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'hello from delete function'
        })
    }