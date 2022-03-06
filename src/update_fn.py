import os, json
import boto3
from pydantic import ValidationError
from BaseModel import base_model

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def update_item(pk,sk, menu_item):
    table_response = table.update_item(
        TableName = table_name,
            Key = {
                'PK': pk,
                'SK': sk                
            },
        ExpressionAttributeNames={
            '#IN': 'item_name',
            '#I': 'ingredients',
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
    return table_response

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    menu_item = base_model.Menu_Item(**body)
    # pk = body['PK']
    # sk = body['SK']
    pk = menu_item.PK
    sk = menu_item.SK
    header = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Content-Type': 'application/json',        
        }
    try:
        response = update_item(pk,sk,menu_item)
        # menu_item = base_model.Menu_Item(**body)
        # table_response = table.update_item(
        #     TableName = table_name,
        #     Key = {
        #         'PK': pk,
        #         'SK': sk                
        #     },
        #     ExpressionAttributeNames={
        #     '#IN': 'item_name',
        #     '#I': 'ingredients',
        #     '#V': 'variations',
        #     '#IMG': 'image',
        #     '#C': 'category'
        #     },
        #     ExpressionAttributeValues={
        #     ':item_name': menu_item.item_name,
        #     ':ingredients': menu_item.ingredients,    
        #     ':variations': menu_item.dict()['variations'],
        #     ':image': menu_item.image,
        #     ':category': menu_item.category
        #     },
        #     UpdateExpression='set #IN = :item_name, #I = :ingredients, #V = :variations, #IMG = :image , #C = :category',
        #     ReturnValues = 'ALL_NEW'
        # )
        # print(table_response)
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