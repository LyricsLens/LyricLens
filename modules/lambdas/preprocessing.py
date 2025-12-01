from typing import List, Dict

#We can move this number up/down but this is to keep us below comprehend limits
MAX_CHARS = 4500


def preprocess_playlist_lyrics(songs: List[Dict[str, str]], max_chars: int = MAX_CHARS) -> str:
    if not songs:
        return ""
    
    #Calculate allocation each song gets (how much weight it has in terms of chars on theme)
    total_songs = len(songs)
    chars_per_song = max_chars // total_songs
    
    #I included this because I would rather have a smaller sample rather than like 2 words per song for longer playlists
    min_sample = 80
    if chars_per_song < min_sample:
        chars_per_song = min_sample
    
    samples = []
    
    #Grab the best sample for each song
    for song in songs:
        lyrics = song.get('lyrics', '')
        if not lyrics:
            continue
        sample = extract_best_sample(lyrics, chars_per_song)
        if sample:
            samples.append(sample)
    
    #Combine 
    combined = '\n\n'.join(samples)

    #If we're still long by the end, snip a bit off
    if len(combined) > max_chars:
        combined = combined[:max_chars]
    
    return combined


def extract_best_sample(lyrics: str, target_chars: int) -> str:
    #Remove junk/stuff we wouldn't keep no matter what
    lyrics = remove_long_lines(lyrics)
    
    if len(lyrics) <= target_chars:
        return lyrics
    
    sections = split_by_sections(lyrics)
    
    #Chorus > First verse > just the beginning if neither are available
    if sections and sections.get('chorus'):
        chorus = sections['chorus'][0]
        if len(chorus) <= target_chars:
            return chorus
        else:
            return truncate_at_line(chorus, target_chars)
    if sections and sections.get('verses'):
        first_verse = sections['verses'][0]
        if len(first_verse) <= target_chars:
            return first_verse
        else:
            return truncate_at_line(first_verse, target_chars)
        
    return truncate_at_line(lyrics, target_chars)

def truncate_at_line(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    last_newline = truncated.rfind('\n')
    if last_newline > max_chars * 0.8:
        return truncated[:last_newline].strip()
    return truncated.strip()

#One of the tests had an insanely long line, this is to prevent anything silly like that
def remove_long_lines(lyrics: str) -> str:
    lines = lyrics.split('\n')
    clean_lines = []
    long_line_streak = 0
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            clean_lines.append('')
            long_line_streak = 0
            continue
        if len(line_stripped) > 200:
            long_line_streak += 1
            if long_line_streak >= 3:
                break  # Stop, not a song
            continue
        clean_lines.append(line)
        long_line_streak = 0
    return '\n'.join(clean_lines)

#Split lyrics by any marked sections and store them accordingly
def split_by_sections(lyrics: str) -> dict:
    sections = {
        'chorus': [],
        'verses': [],
        'bridge': [],
        'intro': [],
        'outro': []
    }
    
    if '[' not in lyrics or ']' not in lyrics:
        return {}
    lines = lyrics.split('\n')
    current_section = 'verses'
    current_content = []
    
    for line in lines:
        if line.strip().startswith('[') and ']' in line:
            if current_content:
                content = '\n'.join(current_content).strip()
                if content:
                    sections[current_section].append(content)
                current_content = []
            label = line.lower()
            if 'chorus' in label:
                current_section = 'chorus'
            elif 'verse' in label:
                current_section = 'verses'
            elif 'bridge' in label:
                current_section = 'bridge'
            elif 'intro' in label:
                current_section = 'intro'
            elif 'outro' in label:
                current_section = 'outro'
        else:
            current_content.append(line)
    if current_content:
        content = '\n'.join(current_content).strip()
        if content:
            sections[current_section].append(content)
    return sections


#Testing with some of the songs we have in playlist_results_example, pruned for ease of use
#if __name__ == "__main__":
    # test_songs = [
    #     {
    #         "title": "Motion Pictures",
    #         "artist": "Serafina Steer",
    #         "lyrics": "Motion Pictures\nCrowds trip up\nShit. Sit down\nTiny lights. Tiny cities\nPut a bit in the film, see how good it is\n\nMe and the girls are still up\nThat would not make a movie\n\nBig screen fades\nSure, it\u2019s a long life\nI was faded out unfeasibly fast; see how I age\nSee how I age\n\nMe and the girls are still up\nThat would not make a movie great\nThat would not set the record straight\n\nThese are not my best intentions\nThat would not make you wait\nWait around for me\n\nSo faraway when it was close to\nI can hold on I can let it pass through\n\nTiny lights, tiny cities\nPut a bit in the film\nSee how good it is\nTiny cities\nPut a bit in the film\nSee how"
    #     },
    #     {
    #         "title": "Tally Ho",
    #         "artist": "The Clean",
    #         "lyrics": "Now, you said it was yesterday, yesterday's another day\nHad a lot of make believe, I don't know if it's you or\nIf it's me oh, I don't know, I don't know\nTally ho, tally ho!\n\nI'll meet you in your fantasy, just anywhere you can obey\nIpsala, Bombay, this is the wrong way\nCause he'll see you I'll go into shock, it's true\nTally ho, tally ho!\n\nWell where are you now?, and where have you been?\nI've been untrue if this has all \"boun\"? you\nBut who are you, yeah, asking me to, I can't tell\n\nNow, you said it was yesterday, yesterday's another day\nHad a lot of make believe, I don't know if it's you or if it's me\nOh, I don't know, I don't know\nTally ho, tally ho!\n\nTally ho, tally ho!"
    #     },
    #     {
    #         "title": "Red Eyes",
    #         "artist": "The War On Drugs",
    #         "lyrics": "[Verse 1]\nCome and see\nWhere I witness everything\nOn my knees\nYou beat it down to get to my soul\nAgainst my will\nAnyone could tell us you're coming\nBaby don't mind\nLeave it on the line, leave it hanging on a rail\n\n[Verse 2]\nCome and ride away\nIt's easier to stick to the old\nSurrounded by the night\nSurrounded by the night, and you don't give in\nBut you abuse my faith\nLosing every time but I don't know where\nYou're on my side again\nSo ride the heat wherever it goes\nI'll be the one to care, woo!\n\n[Chorus]\nYou're all I've got, wait\nDon't wanna let the dark night cover my soul\nWell, you can see it through the darkness coming my way\nWell, we won't get lost inside it all again"
    #     },
    #     {
    #         "title": "Talking Backwards",
    #         "artist": "Real Estate",
    #         "lyrics": "[Verse 1]\nWe can talk for hours\nAnd the line is still engaged\nWe're not getting any closer\nYou're too many miles away\n\n[Chorus]\nAnd I might as well be talking backwards\nAm I making any sense to you?\nAnd the only thing that really matters\nIs the one thing I can't seem to do\n\n[Verse 2]\nWhen the night was over\nAnd the field was lit up bright\nAnd I walked home with you\nNothing I said came out right\n\n[Chorus]\nAnd I might as well be talking backwards\nAm I making any sense to you?\nAnd the only thing that really matters\nIs the one thing I can't seem to do\n\n[Verse 3]\nAnd I might as well be talking backwards\nAm I making any sense to you\nAnd the only thing that really matters\nIs the one thing I can't seem to\nMake sense of this dream\nIt's the one thing I can't seem to do"
    #     },
    #     {
    #         "title": "Archie, Marry Me",
    #         "artist": "Alvvays",
    #         "lyrics": "[Verse 1]\nYou've expressed explicitly your contempt for matrimony\nYou've student loans to pay and will not risk the alimony\nWe spend our days locked in a room, content inside a bubble\nAnd in the nighttime, we go out and scour the streets for trouble\n\n[Chorus]\nHey, hey\nMarry me, Archie\nHey, hey\nMarry me, Archie\n\n[Verse 2]\nDuring the summer, take me sailing out on the Atlantic\nI won't set my sights on other seas, there is no need to panic\nSo honey, take me by the hand and we can sign some papers\nForget the invitations, floral arrangements and bread makers\n\n[Chorus]\nHey, hey\nMarry me, Archie\nHey, hey\nMarry me, Archie\n\n[Bridge]\nToo late to go out\nToo young to stay in\nThey're talking about\nUs living in sin"
    #     },
    #     {
    #         "title": "I Never Glid Before",
    #         "artist": "Gong",
    #         "lyrics": "[Verse 1]\nThe light gets stronger\nAnd all our eyes look yonder to see what's going on\nBut that's all right\nYou'll soon be out of sight and surfing to the sun\nThe moonwheel's turning, the waves unfurling\nYou're learning you're Zero at the centre of the whirlpool\nYou're Aquaman, and in your hand is a watering\u2014\nCan I now or can I not believe it leave it to be\nThe fun gods winking and we're all blinking\nAnd thinking we're sinking in the sea\nYou're in your glider, the tide you're riding inside her\nIs turning with the moony like the sky, boy\n\n[Chorus]\nOkay, you're mister illusion\nSmiling in all the confusion\n'Cause you're still young today\nBefore I start to play\nI'd just like to say:\nNo I never\nNo I never-ever-ever glid before\nI never, oh, no\n\n[Refrain]\nI never ever glid before\nI never ever glid before\nI never ever glid before\nI never ever glid before"
    #     }
    # ]
    
    
    # #Full playlist
    # print("\n1. Testing full "playlist" preprocessing:")
    
    # result = preprocess_playlist_lyrics(test_songs, max_chars=500)
    
    # print(f"   Output length: {len(result)} chars")
    # print(f"   Chars per song allocated: {500 // len(test_songs)} chars")
    # print(f"\n   Combined result (limited to 300 chars, including newlines):")
    # print(f"   {result[:300]}...")
    
    # #Single song
    # print("\n2. Testing single song extraction:")
    # single_song = test_songs[0]
    # print(f"   Song: {single_song['title']}")
    # print(f"   Original length: {len(single_song['lyrics'])} chars")
    
    # sample = extract_best_sample(single_song['lyrics'], target_chars=150)
    # print(f"   Extracted length: {len(sample)} chars")
    # print(f"   Extracted sample:")
    # print(f"   {sample}")
    
    # #Long line removal
    # print("\n3. Testing long line removal:")
    # junk_lyrics = "This is a normal line\n" + "A" * 250 + "\nAnother normal line"
    # print(f"   Input: 3 lines (one is 250 chars)")
    # cleaned = remove_long_lines(junk_lyrics)
    # print(f"   Output lines: {len(cleaned.split(chr(10)))}")
    # print(f"   Long line removed: {'Yes' if len(cleaned) < len(junk_lyrics) else 'No'}")
    
    # #Section splitting
    # print("\n4. Testing section detection:")
    # lyrics_with_sections = test_songs[0]['lyrics']
    # sections = split_by_sections(lyrics_with_sections)
    # print(f"   Found sections:")
    # for section_type, content_list in sections.items():
    #     if content_list:
    #         print(f"   - {section_type}: {len(content_list)} section(s)")
    
    # #Diff playlist sizes
    # print("\n5. Testing different playlist sizes:")
    # for size in [5, 10, 25, 50]:
    #     large_playlist = test_songs * (size // len(test_songs) + 1)
    #     large_playlist = large_playlist[:size]
        
    #     result = preprocess_playlist_lyrics(large_playlist, max_chars=4500)
    #     chars_per_song = 4500 // size
        
    #     print(f"   {size} songs: {len(result)} chars total, {chars_per_song} chars/song allocated")
    