import json
import os  # Add missing import
import dynamodb
from spotify import get_playlist_lyrics

IMAGES = '/images'
SONGS = '/songs'

ALLOWED_ORIGINS = set(
    (os.environ.get("ALLOWED_ORIGINS") or "http://localhost:3000")
    .split(",")
)

def _cors_headers(origin: str | None):
    # If origin is in allowed list, use it; otherwise use wildcard
    allow_origin = origin if origin in ALLOWED_ORIGINS else "*"
    
    # When using wildcard, credentials must be false
    credentials = "true" if origin in ALLOWED_ORIGINS else "false"
    
    return {
        "Access-Control-Allow-Origin": allow_origin,
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Credentials": credentials,
        "Vary": "Origin",  # lets caches vary per origin
    }

def format(code: int, body=None, origin: str | None = None):
    return _resp(code, origin, body)

def _resp(code: int, origin: str | None, body=None):
    out = {"statusCode": code, "headers": _cors_headers(origin)}
    if body is not None:
        out["body"] = json.dumps(body)
    return out

def lambda_handler(event, context):
    headers_in = event.get("headers") or {}
    origin = headers_in.get("origin") or headers_in.get("Origin")
    http_method = event.get("httpMethod")
    path = event.get("resource") or event.get("path")
    
    # Remove this block if API Gateway handles OPTIONS with MOCK integration
    # Uncomment only if you're using Lambda proxy for OPTIONS
    """
    if http_method == "OPTIONS":
        return format(200, origin=origin)  # Pass origin parameter
    """

    # GET /images - return all URLs
    if http_method == "GET" and path == IMAGES:
        return format(200, dynamodb.get_all_images(), origin=origin)

    # GET /images/{id} - return URL by id
    elif http_method == "GET" and path == IMAGES + "/{id}":
        image_id = event['pathParameters']['id']
        images = dynamodb.get_images(image_id)
        if not images:
            return format(404, {"message": "Not found"}, origin=origin)
        return format(200, images, origin=origin)

    # POST /images - add a new URL
    elif http_method == "POST" and path == IMAGES:
        body = json.loads(event['body'])
        result = dynamodb.post_image(body)        
        if result:
            return format(201, {"message": "Image URL added"}, origin=origin)
        return format(400, {"message": "id and url required"}, origin=origin)
    
    # GET /songs - get songs with their lyrics (fixed: should be GET not POST)
    elif http_method == 'GET' and path == SONGS:
        query_params = event.get('queryStringParameters', {})
        playlist_url = query_params.get('playlist_id', False)
        
        if not playlist_url:
            return format(400, {"message": "No Query params supplied. Need playlist_url"}, origin=origin)
        
        lyrics = get_playlist_lyrics(playlist_url)
        if lyrics:
            return format(200, lyrics, origin=origin)
        return format(400, {"message": "Issue getting songs from playlist. Make sure the playlist is public and there are songs."}, origin=origin)
        
    else:
        return format(400, {"message": "Unsupported operation"}, origin=origin)

def main():
    # For local testing
    test_event = {
        "httpMethod": "GET",
        "resource": "/songs",
        "queryStringParameters": {
            "playlist_id": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
        },
        "headers": {
            "origin": "http://localhost:3000"
        }
    }
    response = lambda_handler(test_event, None)
    print(response)

if __name__ == "__main__":
    main()