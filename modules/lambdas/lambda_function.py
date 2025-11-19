import json
import os
import traceback  # Add for better error logging
import dynamodb
import spotify
import asyncio  # Import asyncio for handling async functions
import base64
import boto3
import uuid
from decimal import Decimal
import theme_analysis
from datetime import datetime

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1") # TODO make sure this is not hardcoded (i dont really know how this line works yet)

BEDROCK = '/generate_images' 
IMAGES = '/images'
SONGS = '/songs'

IMAGE_BUCKET = os.environ.get("IMAGE_BUCKET", "")      
BEDROCK_IMAGE_MODEL_ID = os.environ.get(                
    "BEDROCK_IMAGE_MODEL_ID",
    "amazon.titan-image-generator-v2:0"
)
bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)
s3 = boto3.client("s3")
THEMES = '/themes'

# Add logging
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
        "Vary": "Origin",
    }

async def _fully_await_async(obj):
    if asyncio.iscoroutine(obj):
        obj = await obj
    if isinstance(obj, list):
        return [await _fully_await_async(x) for x in obj]
    if isinstance(obj, dict):
        # Await only values that are coroutines
        out = {}
        for k, v in obj.items():
            out[k] = await _fully_await_async(v)
        return out
    # tuples? sets? keep structure JSON-safe later
    return obj

def fully_await(obj):
    # Runs a small event loop to resolve any nested coroutines
    return asyncio.run(_fully_await_async(obj))

def _json_default(x):
    if isinstance(x, set):
        return list(x)
    if isinstance(x, bytes):
        return base64.b64encode(x).decode("ascii")
    if isinstance(x, Decimal):
        return float(x)
    # last resort string-ify custom objects
    return str(x)

def format(code: int, body=None, origin: str | None = None):
    return _resp(code, origin, body)

def _resp(code: int, origin: str | None, body=None):
    out = {"statusCode": code, "headers": _cors_headers(origin)}
    if body is not None:
        out["body"] = json.dumps(body, default=_json_default)
    return out

def lambda_handler(event, context):
    try:
        # Log the incoming event for debugging
        logger.info(f"Received event: {json.dumps(event)}")
        
        headers_in = event.get("headers") or {}
        origin = headers_in.get("origin") or headers_in.get("Origin")
        http_method = event.get("httpMethod")
        path = event.get("resource") or event.get("path")
        
        logger.info(f"Method: {http_method}, Path: {path}, Origin: {origin}")
        
        # API Gateway handles OPTIONS with MOCK integration, so this shouldn't be reached
        # But if it is, handle it gracefully
        if http_method == "OPTIONS":
            logger.info("Handling OPTIONS request in Lambda")
            return format(200, origin=origin)

        # ================ IMAGES  ================

        # GET /images - return all URLs
        if http_method == "GET" and path == IMAGES:
            logger.info("Getting all images")
            images = dynamodb.get_all_images()
            return format(200, images, origin=origin)

        # GET /images/{id} - return URL by id
        elif http_method == "GET" and path == IMAGES + "/{id}":
            image_id = event['pathParameters']['id']
            logger.info(f"Getting image with id: {image_id}")
            images = dynamodb.get_images(image_id)
            if not images:
                return format(404, {"message": "Not found"}, origin=origin)
            return format(200, images, origin=origin)

        # POST /images - add a new URL
        elif http_method == "POST" and path == IMAGES:
            body = json.loads(event['body'])
            logger.info(f"Posting new image: {body}")
            result = dynamodb.post_image(body)        
            if result:
                return format(201, {"message": "Image URL added"}, origin=origin)
            return format(400, {"message": "id and url required"}, origin=origin)
        
        # ================ SONGS ================

        # GET /songs - get songs with their lyrics
        elif http_method == 'GET' and path == SONGS:
            query_params = event.get('queryStringParameters') or {}
            playlist_id = query_params.get('playlist_id')

            logger.info(f"Getting songs for playlist: {playlist_id}")

            if not playlist_id:
                return format(400, {"message": "No Query params supplied. Need playlist_id"}, origin=origin)

            try:
                # maybe_coro = get_playlist_lyrics_async(playlist_url)
                # top_level = asyncio.run(maybe_coro) if asyncio.iscoroutine(maybe_coro) else maybe_coro

                # # 🔧 NEW: resolve any nested coroutines produced inside the async function
                # lyrics = fully_await(top_level)
                lyrics = spotify.get_playlist_lyrics(playlist_id)
                logger.info(f"Retrieved lyrics: {bool(lyrics)}; type={type(lyrics)}")

                if lyrics:
                    return format(200, lyrics, origin=origin)
                else:
                    return format(
                        400,
                        {"message": "Issue getting songs from playlist. Make sure the playlist is public and there are songs."},
                        origin=origin,
                    )
            except Exception as e:
                logger.error(f"Error getting playlist lyrics: {str(e)}")
                logger.error(traceback.format_exc())
                return format(500, {"message": f"Error retrieving playlist: {str(e)}"}, origin=origin)
        #GET /themes - get theme analysis for playlist
        elif http_method == 'GET' and path == THEMES:
            query_params = event.get('queryStringParameters') or {}
            playlist_id = query_params.get('playlist_id')

            logger.info(f"Getting themes for playlist: {playlist_id}")

            if not playlist_id:
                return format(400, {"message": "No Query params supplied. Need playlist_id"}, origin=origin)

            try:
                lyrics = spotify.get_playlist_lyrics(playlist_id)
                logger.info(f"Retrieved {len(lyrics)} songs")

                if lyrics:
                    themes = theme_analysis.analyze_playlist_themes(lyrics)
                    return format(200, themes, origin=origin)
                else:
                    return format(
                        400,
                        {"message": "Issue getting songs from playlist. Make sure the playlist is public and there are songs."},
                        origin=origin,
                    )
            except Exception as e:
                logger.error(f"Error analyzing themes: {str(e)}")
                logger.error(traceback.format_exc())
                return format(500, {"message": f"Error analyzing themes: {str(e)}"}, origin=origin)

        # ================ BEDROCK IMAGE GENERATION ================

        elif http_method == "POST" and path == BEDROCK:
            logger.info("Handling Bedrock image generation.")
            return handle_bedrock_image(event, origin)

        else:
            logger.warning(f"Unsupported operation: {http_method} {path}")
            return format(400, {"message": f"Unsupported operation: {http_method} {path}"}, origin=origin)

    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "statusCode": 500,
            "headers": _cors_headers(origin if 'origin' in locals() else None),
            "body": json.dumps({"message": "Internal server error", "error": str(e)}),
        }

def handle_bedrock_image(event, origin):
    # handles request to generate images using bedrock. current way to generate images is to just plop in a string, but in the future we can use keywords maybe
    """
    Example request:
      POST /generate_images
      body: {
        "prompt": "angsty frog in a neon city",
        "width": 512,       # optional
        "height": 512,      # optional
        "cfgScale": 8,      # optional
        "seed": 1234        # optional
      }

    Example response:
      {
        "id": "...",
        "url": "https://bucket.s3.region.amazonaws.com/path.png"
      }
      OR if no IMAGE_BUCKET is set:
      {
        "imageBase64": "...",
        "prompt": "..."
      }
    """
    body = event.get("body")
    if not body:
        return format(400, {"message": "Missing body"}, origin=origin)

    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return format(400, {"message": "Invalid JSON body"}, origin=origin)

    prompt = payload.get("prompt")
    if not prompt:
        return format(400, {"message": "Field 'prompt' is required"}, origin=origin)

    width = int(payload.get("width", 512))
    height = int(payload.get("height", 512))
    cfg_scale = float(payload.get("cfgScale", 8.0))
    seed = int(payload.get("seed", 1234))

    logger.info(
        f"[Bedrock] Generating image... prompt='{prompt[:60]}...', "
        f"w={width}, h={height}, cfgScale={cfg_scale}, seed={seed}"
    )

    request_body = {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": prompt
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "height": height,
            "width": width,
            "cfgScale": cfg_scale,
            "quality": "standard",
            "seed": seed,
        }
    }

    try:
        response = bedrock.invoke_model(
            modelId=BEDROCK_IMAGE_MODEL_ID,
            body=json.dumps(request_body),
            contentType="application/json",
            accept="application/json",
        )

        response_body = json.loads(response["body"].read())
        images = response_body.get("images") or []

        if not images:
            logger.error(f"[Bedrock] No images returned: {response_body}")
            return format(500, {"message": "No image returned from Bedrock"}, origin=origin)

        image_b64 = images[0]
        image_bytes = base64.b64decode(image_b64)

        # If no bucket configured, just return base64
        if not IMAGE_BUCKET:
            return format(200, {
                "imageBase64": image_b64,
                "prompt": prompt,
            }, origin=origin)

        # Otherwise, store in S3 and return URL
        image_id = str(uuid.uuid4())
        key = f"generated/{image_id}.png"

        s3.put_object(
            Bucket=IMAGE_BUCKET,
            Key=key,
            Body=image_bytes,
            ContentType="image/png",
        )

        url = f"https://{IMAGE_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{key}"

        # saving to dynamo
        try:
            dynamodb.post_image({
                "id": image_id,
                "url": url,
                "prompt": prompt,
                "width": width,
                "height": height,
                "cfgScale": cfg_scale,
                "seed": seed,
                "createdAt": datetime.utcnow().isoformat() + "Z",
            })
        except Exception as e:
            logger.error(f"Failed to save image metadata to DynamoDB: {e}")

        return format(200, {
            "id": image_id,
            "url": url,
            "bucket": IMAGE_BUCKET,
            "key": key,
        }, origin=origin)

    except Exception as e:
        logger.error(f"[Bedrock] Exception during image generation: {str(e)}")
        logger.error(traceback.format_exc())
        return format(500, {"message": "Error generating image", "error": str(e)}, origin=origin)


def main():
    # For local testing
    test_event = {
        "httpMethod": "GET",
        "resource": "/songs",
        "queryStringParameters": {
            "playlist_id": "0ZS0e1UXYRFxZfkBTEGnk4"
        },
        "headers": {
            "origin": "http://localhost:3000"
        }
    }
    response = lambda_handler(test_event, None)
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()