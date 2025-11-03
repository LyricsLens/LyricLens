import json
import dynamodb
from spotify import get_playlist_lyrics

IMAGES = '/images'
SONGS = '/songs'

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",  # or set to your S3 URL for security
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}

def format(code: int, body = None):
    result = {
        "statusCode": code,
        "headers": CORS_HEADERS,
    }

    if body:
        result['body'] = json.dumps(body)

    return result

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['resource']

    if http_method == "OPTIONS":
        return format(200)

    # GET /images - return all URLs
    if http_method == "GET" and path == IMAGES:
       return format(200, dynamodb.get_all_images())

    # GET /images/{id} - return URL by id
    elif http_method == "GET" and path == IMAGES + "/{id}":
        image_id = event['pathParameters']['id']
        images = dynamodb.get_images(image_id)
        if not images:
            return format(404, {"message": "Not found"})
        return format(200, images)

    # POST /images - add a new URL
    elif http_method == "POST" and path == IMAGES:
        body = json.loads(event['body'])
        result = dynamodb.post_image(body)        
        if result:
            return format(201, {"message": "Image URL added"})
        return format(400, {"message": "id and url required"})
    
    # POST /songs - get songs with their lyrics
    elif http_method == 'GET' and path == SONGS:
        query_params = event.get('queryStringParameters', {})
        playlist_url = query_params.get('playlist_id', False)
        lyrics = get_playlist_lyrics(playlist_url)
        if not playlist_url:
            return format(400, {"message": "No Query params supplied. Need playlist_url"})
        if lyrics:
            return format(200, lyrics)
        return format(400, {"message": "Issue getting songs from playlist. Make sure the playlist is public and there are songs."})
        
    else:
        return {"statusCode": 400, "body": json.dumps({"message": "Unsupported operation"})}

# def lambda_handler(event, context):
#     http_method = event['httpMethod']
#     path = event['resource']

#         # Handle preflight OPTIONS request
#     if http_method == "OPTIONS":
#         return {
#             "statusCode": 200,
#             "headers": CORS_HEADERS,
#             "body": ""
#     }

    
#     # GET /images - return all URLs
#     if http_method == "GET" and path == "/images":
#         response = table.scan()
#         return {
#             "statusCode": 200,
#             "headers": CORS_HEADERS,
#             "body": json.dumps(response.get('Items', []))
#         }

#     # GET /images/{id} - return URL by id
#     elif http_method == "GET" and path == "/images/{id}":
#         image_id = event['pathParameters']['id']
#         response = table.get_item(Key={"id": image_id})
#         if 'Item' in response:
#             return {"statusCode": 200, "headers": CORS_HEADERS, "body": json.dumps(response['Item'])}
#         return {"statusCode": 404, "headers": CORS_HEADERS, "body": json.dumps({"message": "Not found"})}

#     # POST /images - add a new URL
#     elif http_method == "POST" and path == "/images":
#         body = json.loads(event['body'])
#         if 'id' not in body or 'url' not in body:
#             return {"statusCode": 400, "headers": CORS_HEADERS, "body": json.dumps({"message": "id and url required"})}
#         table.put_item(Item={"id": body['id'], "url": body['url']})
#         return {"statusCode": 201, "headers": CORS_HEADERS, "body": json.dumps({"message": "Image URL added"})}

#     else:
#         return {"statusCode": 400, "headers": CORS_HEADERS, "body": json.dumps({"message": "Unsupported operation"})}