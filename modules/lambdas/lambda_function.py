import json
import dynamodb
from spotify import get_playlist_lyrics

IMAGES = '/images'
SONGS = '/songs'


def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['resource']

    # GET /images - return all URLs
    if http_method == "GET" and path == IMAGES:
       return dynamodb.get_all_images()

    # GET /images/{id} - return URL by id
    elif http_method == "GET" and path == IMAGES + "/{id}":
        image_id = event['pathParameters']['id']
        return dynamodb.get_images(image_id)

    # POST /images - add a new URL
    elif http_method == "POST" and path == IMAGES:
        body = json.loads(event['body'])
        return dynamodb.post_image(body)        
    
    # POST /songs - get songs with their lyrics
    elif http_method == 'GET' and path == SONGS:
        query_params = event.get('queryStringParameters', {})
        playlist_url = query_params.get('playlist_url', False)
        if not playlist_url:
            return {"statusCode": 400, "body": json.dumps({"message": "No Query params supplied. Need playlist_url"})}
        
        return get_playlist_lyrics(playlist_url)

    else:
        return {"statusCode": 400, "body": json.dumps({"message": "Unsupported operation"})}
