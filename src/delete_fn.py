import json
import boto3
import os

from pydantic import ValidationError
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("TABLE_NAME")
table = dynamodb.Table(table_name)


def delete_item(pk, sk):
    table_response = table.delete_item(
        TableName=table_name,
        Key={"PK": pk, "SK": sk},
        # ConditionExpression = 'attribute_exists(PK) & attribute_exists(SK)'
    )
    print(table_response)
    return table_response


def lambda_handler(event, context):
    print(event)
    body = json.loads(event["body"])
    pk = body["pk"]
    sk = body["sk"]

    header = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
    }
    try:
        response = delete_item(pk, sk)
        print(response)
        return {
            "statusCode": 200,
            "headers": header,
            "body": json.dumps(
                {
                    "error": False,
                    "code": "ITEM_DELETED",
                    "message": "Deleted single item",
                }
            ),
        }
    except ValidationError as e:
        return {
            "statusCode": 400,
            "headers": header,
            "body": json.dumps(
                {"error": True, "code": "VALIDATION_ERROR", "message": str(e)}
            ),
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 400,
            "headers": header,
            "body": json.dumps(
                {
                    "error": True,
                    "code": "UNKNOWN_ERROR",
                    "message": "Some error occured.Please try again.",
                }
            ),
        }
