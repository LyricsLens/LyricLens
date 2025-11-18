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
    
    return {
        'key_phrases': comprehend_data['key_phrases'],
        'entities': comprehend_data['entities'],
        'sentiment': comprehend_data['sentiment'],
        'sentiment_scores': comprehend_data.get('sentiment_scores', {}),
        'total_songs_analyzed': len(songs),
        'preview_text': combined_lyrics[:200] + "..." #TODO: just for debugging, this line can be removed after testing
    }


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


#Simple test
if __name__ == "__main__":
    test_songs = [
        {
            "title": "Motion Pictures",
            "artist": "Serafina Steer",
            "lyrics": "Motion Pictures\nCrowds trip up\nShit. Sit down\nTiny lights. Tiny cities\nPut a bit in the film, see how good it is\n\nMe and the girls are still up\nThat would not make a movie\n\nBig screen fades\nSure, it\u2019s a long life\nI was faded out unfeasibly fast; see how I age\nSee how I age\n\nMe and the girls are still up\nThat would not make a movie great\nThat would not set the record straight\n\nThese are not my best intentions\nThat would not make you wait\nWait around for me\n\nSo faraway when it was close to\nI can hold on I can let it pass through\n\nTiny lights, tiny cities\nPut a bit in the film\nSee how good it is\nTiny cities\nPut a bit in the film\nSee how"
        },
        {
            "title": "Tally Ho",
            "artist": "The Clean",
            "lyrics": "Now, you said it was yesterday, yesterday's another day\nHad a lot of make believe, I don't know if it's you or\nIf it's me oh, I don't know, I don't know\nTally ho, tally ho!\n\nI'll meet you in your fantasy, just anywhere you can obey\nIpsala, Bombay, this is the wrong way\nCause he'll see you I'll go into shock, it's true\nTally ho, tally ho!\n\nWell where are you now?, and where have you been?\nI've been untrue if this has all \"boun\"? you\nBut who are you, yeah, asking me to, I can't tell\n\nNow, you said it was yesterday, yesterday's another day\nHad a lot of make believe, I don't know if it's you or if it's me\nOh, I don't know, I don't know\nTally ho, tally ho!\n\nTally ho, tally ho!"
        },
        {
            "title": "Red Eyes",
            "artist": "The War On Drugs",
            "lyrics": "[Verse 1]\nCome and see\nWhere I witness everything\nOn my knees\nYou beat it down to get to my soul\nAgainst my will\nAnyone could tell us you're coming\nBaby don't mind\nLeave it on the line, leave it hanging on a rail\n\n[Verse 2]\nCome and ride away\nIt's easier to stick to the old\nSurrounded by the night\nSurrounded by the night, and you don't give in\nBut you abuse my faith\nLosing every time but I don't know where\nYou're on my side again\nSo ride the heat wherever it goes\nI'll be the one to care, woo!\n\n[Chorus]\nYou're all I've got, wait\nDon't wanna let the dark night cover my soul\nWell, you can see it through the darkness coming my way\nWell, we won't get lost inside it all again"
        },
        {
            "title": "Talking Backwards",
            "artist": "Real Estate",
            "lyrics": "[Verse 1]\nWe can talk for hours\nAnd the line is still engaged\nWe're not getting any closer\nYou're too many miles away\n\n[Chorus]\nAnd I might as well be talking backwards\nAm I making any sense to you?\nAnd the only thing that really matters\nIs the one thing I can't seem to do\n\n[Verse 2]\nWhen the night was over\nAnd the field was lit up bright\nAnd I walked home with you\nNothing I said came out right\n\n[Chorus]\nAnd I might as well be talking backwards\nAm I making any sense to you?\nAnd the only thing that really matters\nIs the one thing I can't seem to do\n\n[Verse 3]\nAnd I might as well be talking backwards\nAm I making any sense to you\nAnd the only thing that really matters\nIs the one thing I can't seem to\nMake sense of this dream\nIt's the one thing I can't seem to do"
        },
        {
            "title": "Archie, Marry Me",
            "artist": "Alvvays",
            "lyrics": "[Verse 1]\nYou've expressed explicitly your contempt for matrimony\nYou've student loans to pay and will not risk the alimony\nWe spend our days locked in a room, content inside a bubble\nAnd in the nighttime, we go out and scour the streets for trouble\n\n[Chorus]\nHey, hey\nMarry me, Archie\nHey, hey\nMarry me, Archie\n\n[Verse 2]\nDuring the summer, take me sailing out on the Atlantic\nI won't set my sights on other seas, there is no need to panic\nSo honey, take me by the hand and we can sign some papers\nForget the invitations, floral arrangements and bread makers\n\n[Chorus]\nHey, hey\nMarry me, Archie\nHey, hey\nMarry me, Archie\n\n[Bridge]\nToo late to go out\nToo young to stay in\nThey're talking about\nUs living in sin"
        },
        {
            "title": "I Never Glid Before",
            "artist": "Gong",
            "lyrics": "[Verse 1]\nThe light gets stronger\nAnd all our eyes look yonder to see what's going on\nBut that's all right\nYou'll soon be out of sight and surfing to the sun\nThe moonwheel's turning, the waves unfurling\nYou're learning you're Zero at the centre of the whirlpool\nYou're Aquaman, and in your hand is a watering\u2014\nCan I now or can I not believe it leave it to be\nThe fun gods winking and we're all blinking\nAnd thinking we're sinking in the sea\nYou're in your glider, the tide you're riding inside her\nIs turning with the moony like the sky, boy\n\n[Chorus]\nOkay, you're mister illusion\nSmiling in all the confusion\n'Cause you're still young today\nBefore I start to play\nI'd just like to say:\nNo I never\nNo I never-ever-ever glid before\nI never, oh, no\n\n[Refrain]\nI never ever glid before\nI never ever glid before\nI never ever glid before\nI never ever glid before"
        }
    ]
    
    result = analyze_playlist_themes(test_songs)
    
    print(f"\nTotal songs: {result['total_songs_analyzed']}")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Sentiment scores: {result.get('sentiment_scores', {})}")
    
    print(f"\nTop Key Phrases ({len(result['key_phrases'])}):")
    for phrase in result['key_phrases'][:10]:
        print(f"  - {phrase['text']} (confidence: {phrase['score']})")
    
    print(f"\nTop Entities ({len(result['entities'])}):")
    for entity in result['entities'][:10]:
        print(f"  - {entity['text']} [{entity['type']}] (confidence: {entity['score']})")
    
    print(f"\nPreview text:")
    print(f"  {result.get('preview_text', 'N/A')}")
    
    print("Full JSON output:")
    print(json.dumps(result, indent=2))