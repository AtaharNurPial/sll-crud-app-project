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
    pk = menu_item.PK
    sk = menu_item.SK
    header = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*',
    }
    try:
        response = update_item(pk,sk,menu_item)
        return{
            'statusCode': 200,
            'headers': header,
            'body': json.dumps({
                'error': False,
                'code': 'UPDATE_SUCCESSFUL',
                'message': 'Item updated Successfully',
                'value': response
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
    except Exception as e:
        print(e)
        return{
            'statusCode': 400,
            'headers': header,
            'body': json.dumps({
            'error': True,
            'code': 'UNKNOWN_ERROR',
            'message': 'Some error occured. Please try again.'
            })
        }    