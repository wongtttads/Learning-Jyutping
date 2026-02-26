import requests
import pandas as pd
import ToJyutping
import re
import os

# GitHub raw URLs for the character lists
BASE_URL = "https://raw.githubusercontent.com/shengdoushi/common-standard-chinese-characters-table/master/"
LEVELS = {
    1: "level-1.txt",
    2: "level-2.txt",
    3: "level-3.txt"
}

# LSHK Jyutping finals (including those with codas)
FINALS = [
    'aa', 'aai', 'aau', 'aam', 'aan', 'aang', 'aap', 'aat', 'aak',
    'ai', 'au', 'am', 'an', 'ang', 'ap', 'at', 'ak',
    'e', 'ei', 'eu', 'em', 'en', 'eng', 'ep', 'et', 'ek',
    'i', 'iu', 'im', 'in', 'ing', 'ip', 'it', 'ik',
    'o', 'oi', 'ou', 'on', 'ong', 'ot', 'ok',
    'u', 'ui', 'un', 'ung', 'ut', 'uk',
    'oe', 'oeng', 'oet', 'oek',
    'eo', 'eoi', 'eon', 'eot',
    'yu', 'yun', 'yut',
    'm', 'ng'
]

def get_character_list(level):
    url = BASE_URL + LEVELS[level]
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Filter out empty lines and whitespace
        chars = [c.strip() for c in response.text if c.strip()]
        return chars
    except Exception as e:
        print(f"Error fetching level {level}: {e}")
        return []

def parse_jyutping(jp_str):
    """
    Parses a Jyutping string into (onset, final, tone).
    Example: 'ho2' -> ('h', 'o', '2')
    'aa1' -> ('', 'aa', '1')
    """
    if not jp_str:
        return None, None, None
    
    # Extract tone (last character)
    match = re.search(r'([a-z]+)([1-6])$', jp_str)
    if not match:
        return None, None, None
    
    syllable = match.group(1)
    tone = match.group(2)
    
    # Extract onset and final
    # Longest match for finals
    found_final = None
    found_onset = None
    
    # Try matching from the end of the syllable
    for f in sorted(FINALS, key=len, reverse=True):
        if syllable.endswith(f):
            found_final = f
            found_onset = syllable[:-len(f)]
            break
            
    return found_onset, found_final, tone

def build_db():
    all_data = []
    
    for level, filename in LEVELS.items():
        print(f"Processing Level {level}...")
        chars = get_character_list(level)
        
        for i, char in enumerate(chars):
            # ToJyutping.get_jyutping_candidates returns [ (char, [jp1, jp2, ...]) ]
            candidates = ToJyutping.get_jyutping_candidates(char)
            
            # The structure is [ (char, [jps]) ]
            jp = None
            jps = None
            if candidates:
                char_res, jps = candidates[0]
            
            onset, final, tone = None, None, None
            
            if jps:
                jp = jps[0]
                onset, final, tone = parse_jyutping(jp)
            
            all_data.append({
                'char': char,
                'jyutping': jp,
                'onset': onset,
                'final': final,
                'tone': tone,
                'level': level,
                'frequency_rank': i + 1,  # Using position in table as rank
                'status': 'standard' if jp else 'missing_pinyin'
            })
    
    df = pd.DataFrame(all_data)
    
    # Output path
    output_path = 'data/processed/jyutping_master.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Database built successfully: {output_path}")
    print(f"Total characters processed: {len(df)}")

if __name__ == "__main__":
    build_db()
