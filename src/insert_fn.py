
import json
from BaseModel import base_model

result = base_model.display()

def lambda_handler(event, context):
    print(event)
    header = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Content-Type': 'application/json',        
    }
    return{
        'statusCode': 200,
        'headers': header,
        'body': json.dumps({
            'message': result
        })
    }