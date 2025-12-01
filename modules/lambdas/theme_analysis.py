import boto3
import json
import logging
from typing import Dict, List, Any
from preprocessing import preprocess_playlist_lyrics

logger = logging.getLogger(__name__)
comprehend = boto3.client('comprehend', region_name='us-east-1')


def analyze_playlist_themes(songs: List[Dict[str, str]]) -> Dict[str, Any]:
    if not songs:
        return {
            'error': 'No songs provided, this playlist may be empty.',
            'key_phrases': [],
            'entities': [],
            'sentiment': 'NEUTRAL'
        }
    
    logger.info(f"Analyzing {len(songs)} songs in the playlist" )
    
    combined_lyrics = preprocess_playlist_lyrics(songs, max_chars=4500)
    
    if not combined_lyrics:
        return {
            'error': 'No valid lyrics found, this playlist may only have instrumentals.',
            'key_phrases': ['instrumental'],
            'entities': [],
            'sentiment': 'NEUTRAL'
        }
    
    logger.info(f"Combined lyrics: {len(combined_lyrics)} chars")
    comprehend_data = extract_themes_from_comprehend(combined_lyrics)
    
    formatted_response = format_theme_response(
        comprehend_data,
        len(songs),
        combined_lyrics
    )

    return formatted_response


def extract_themes_from_comprehend(text: str) -> Dict[str, Any]:
    if not text or not text.strip():
        return {
            'key_phrases': [],
            'entities': [],
            'sentiment': 'NEUTRAL',
            'sentiment_scores': {}
        }
    
    try:
        logger.info("Calling Comprehend: detect_key_phrases")
        key_phrases_response = comprehend.detect_key_phrases(
            Text=text,
            LanguageCode='en'
        )
        logger.info("Calling Comprehend: detect_entities")
        entities_response = comprehend.detect_entities(
            Text=text,
            LanguageCode='en'
        )
        logger.info("Calling Comprehend: detect_sentiment")
        sentiment_response = comprehend.detect_sentiment(
            Text=text,
            LanguageCode='en'
        )
        key_phrases = [
            {
                'text': phrase['Text'],
                'score': round(phrase['Score'], 3)
            }
            for phrase in sorted(
                key_phrases_response['KeyPhrases'],
                key=lambda x: x['Score'],
                reverse=True
            )
            #This is to only grab phrases with high confidences
            if phrase['Score'] > 0.7
        ]
        entities = [
            {
                'text': entity['Text'],
                'type': entity['Type'],
                'score': round(entity['Score'], 3)
            }
            for entity in sorted(
                entities_response['Entities'],
                key=lambda x: x['Score'],
                reverse=True
            )
            if entity['Score'] > 0.6
        ]
        
        logger.info(f"Found {len(key_phrases)} key phrases, {len(entities)} entities")
        
        return {
            'key_phrases': key_phrases[:30],
            'entities': entities[:20],
            'sentiment': sentiment_response['Sentiment'],
            'sentiment_scores': sentiment_response['SentimentScore']
        }
        
    except Exception as e:
        logger.error(f"Error calling Comprehend: {str(e)}")
        return {
            'key_phrases': ['Error'],
            'entities': [],
            'sentiment': 'NEUTRAL',
            'sentiment_scores': {},
            'error': str(e)
        }

def format_theme_response(comprehend_data: Dict[str, Any],total_songs: int,preview_text: str) -> Dict[str, Any]:
    #uhh don't mind the params sorry

    key_phrases = comprehend_data.get('key_phrases', [])
    entities = comprehend_data.get('entities', [])
    sentiment = comprehend_data.get('sentiment', 'NEUTRAL')
    sentiment_scores = comprehend_data.get('sentiment_scores', {})
    
    locations = []
    people = []
    organizations = []
    dates_times = []
    quantities = []
    
    for e in entities:
        entity_type = e.get('type', '')
        entity_text = e.get('text', '')
        
        if entity_type == 'LOCATION':
            locations.append(entity_text)
        elif entity_type == 'PERSON':
            people.append(entity_text)
        elif entity_type == 'ORGANIZATION':
            organizations.append(entity_text)
        elif entity_type == 'DATE':
            dates_times.append(entity_text)
        elif entity_type == 'QUANTITY':
            quantities.append(entity_text)
    
    top_themes = [p['text'] for p in key_phrases[:10]]
    
    vibe = generate_vibe_description(top_themes, locations, sentiment)
    
    return {
        'playlist_summary': {
            'total_songs': total_songs,
            'overall_vibe': vibe,
            'sentiment': {
                'primary': sentiment,
            }
        },
        'top_themes': top_themes,
        'locations_mentioned': locations[:8],
        'people_mentioned': people[:5],
        'organizations_brands': organizations[:5],
        'time_references': dates_times[:5],
        'quantities_mentioned': quantities[:5],
        'raw_data': {
            'all_key_phrases': key_phrases[:30],
            'all_entities': entities[:20]
        },
        'lyric_preview': preview_text[:200] + "..." if len(preview_text) > 200 else preview_text
    }


def generate_vibe_description(themes: List[str],locations: List[str],sentiment: str) -> str:
    #We can use this or just throw it out, vibe for a concise topic combination for prompts
    sentiment_desc = {
        'POSITIVE': 'upbeat and energetic',
        'NEGATIVE': 'melancholic and introspective',
        'NEUTRAL': 'balanced and contemplative',
        'MIXED': 'emotionally complex'
    }.get(sentiment, 'varied')
    
    #top 2-3 themes to describe the vibe, default to whatever's there otherwise
    if len(themes) >= 2:
        theme_descriptors = themes[:2]
        theme_str = ' & '.join(theme_descriptors)
        return f"{sentiment_desc} {theme_str} vibes"
    elif len(themes) == 1:
        return f"{sentiment_desc} {themes[0]} vibes"
    else:
        return f"{sentiment_desc} vibes"