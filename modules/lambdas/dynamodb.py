import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ['TABLE_NAME'])

def get_all_images():
    response = table.scan()
    return response.get('Items', [])

def get_images(image_id: str):
    response = table.get_item(Key={"id": image_id})
    if 'Item' in response:
        return response['Item']
    return False

def post_image(body: dict):
    if 'id' not in body or 'url' not in body:
        return False
    table.put_item(Item=body)
    return True