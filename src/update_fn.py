from typing import List
import os
import boto3
import json
from pydantic import ValidationError
from BaseModel import base_model
# from BaseModel.base_model import Menu_Item

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
client = dynamodb.Table(table_name)

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    pk = body['PK']
    sk = body['SK']
    header = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Content-Type': 'application/json',        
        }
    try:
        menu_item = base_model.Menu_Item(**body)
        table_response = client.update_item(
            TableName = table_name,
            Key = {
                'PK': pk,
                'SK': sk                
            },
            ExpressionAttributeNames={
            '#IN': 'item_name',
            # '#I': 'ingredients',
            '#V': 'variations',
            '#IMG': 'image',
            '#C': 'category'
            },
            ExpressionAttributeValues={
            ':item_name': menu_item.item_name,
            ':ingredients': menu_item.ingredients,    
            ':variations': menu_item.dict()['variations'],
            ':image': menu_item.image,
            ':category': menu_item.category
            },
            UpdateExpression='set #IN = :item_name, #I = :ingredients, #V = :variations, #IMG = :image , #C = :category',
            ReturnValues = 'ALL_NEW'
        )
        print(table_response)
        return{
            'statusCode': 200,
            'headers': header,
            'body': json.dumps({
                'message': 'Item updated Successfully',
                'value': menu_item.dict()
            })
        }
    except ValidationError as e:
        return{
            'statusCode': 400,
            'headers': header,
            'body': json.dumps({
                'message': str(e)
            })
        }