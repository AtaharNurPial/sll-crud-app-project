import boto3
import json
from pydantic import ValidationError
from BaseModel import base_model
from BaseModel.base_model import Menu_Item
import os
# result = base_model.display()
table_name = os.environ.get('TABLE_NAME')
default_headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Headers": "*",
}


def lambda_handler(event, context):
    print(event)
    body = event["body"]
    print(body)
    body = json.loads(body)
    # print(type(body))
    try:
        menu_item = Menu_Item(**body)
    except ValidationError as e:
        return{
            'statusCode': 400,
            'headers': default_headers,
            'body': json.dumps({
                'message': str(e)
            })
        }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.put_item(
        Item=menu_item.dict()
    )

    return {
        "statusCode": 200,
        "headers": default_headers,
        "body": json.dumps({
            "message": "Item Inserted",
            "item": menu_item.dict(),

        })



        # "item": menu_item.json()
        # "location": ip.text.replace("\n", "")

    }
