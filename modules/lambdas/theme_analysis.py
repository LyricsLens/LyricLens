import boto3
from typing import Dict, List, Any
from preprocessing import preprocess_playlist_lyrics

#New to me -- basically allows interaction w comprehend without client calls. Can change if needed.
comprehend = boto3.client('comprehend', region_name='us-east-1')


def analyze_playlist_themes(songs: List[Dict[str, str]]) -> Dict[str, Any]:
    if not songs:
        return {
            'error': 'No songs provided',
            'key_phrases': [],
            'entities': [],
            'sentiment': 'NEUTRAL'
        }
    else:
        #TODO
        return {}