import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ['TABLE_NAME'])

def get_all_images():
    response = table.scan()
    return {
        "statusCode": 200,
        "body": json.dumps(response.get('Items', []))
    }

def get_images(image_id: str):
    response = table.get_item(Key={"id": image_id})
    if 'Item' in response:
        return {"statusCode": 200, "body": json.dumps(response['Item'])}
    return {"statusCode": 404, "body": json.dumps({"message": "Not found"})}    

def post_image(body: dict):
    if 'id' not in body or 'url' not in body:
        return {"statusCode": 400, "body": json.dumps({"message": "id and url required"})}
    table.put_item(Item={"id": body['id'], "url": body['url']})
    return {"statusCode": 201, "body": json.dumps({"message": "Image URL added"})}