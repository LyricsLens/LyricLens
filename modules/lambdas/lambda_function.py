import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['resource']

    # GET /images - return all URLs
    if http_method == "GET" and path == "/images":
        response = table.scan()
        return {
            "statusCode": 200,
            "body": json.dumps(response.get('Items', []))
        }

    # GET /images/{id} - return URL by id
    elif http_method == "GET" and path == "/images/{id}":
        image_id = event['pathParameters']['id']
        response = table.get_item(Key={"id": image_id})
        if 'Item' in response:
            return {"statusCode": 200, "body": json.dumps(response['Item'])}
        return {"statusCode": 404, "body": json.dumps({"message": "Not found"})}

    # POST /images - add a new URL
    elif http_method == "POST" and path == "/images":
        body = json.loads(event['body'])
        if 'id' not in body or 'url' not in body:
            return {"statusCode": 400, "body": json.dumps({"message": "id and url required"})}
        table.put_item(Item={"id": body['id'], "url": body['url']})
        return {"statusCode": 201, "body": json.dumps({"message": "Image URL added"})}

    else:
        return {"statusCode": 400, "body": json.dumps({"message": "Unsupported operation"})}
