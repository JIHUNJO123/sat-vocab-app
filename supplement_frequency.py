"""
빈도수 기반 일본어 단어 보충 스크립트

이 스크립트는 일본어 코퍼스 빈도수 데이터를 활용하여
JLPT 데이터를 보충합니다.

빈도수 데이터 소스:
- Wikipedia Japanese corpus
- Japanese subtitles corpus
- News corpus

상업적 사용 가능한 소스만 사용합니다.
"""

import json
import os
import requests
from typing import Dict, List, Set, Tuple


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'raw_data')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def download_frequency_lists():
    """다양한 빈도수 리스트 다운로드"""
    
    sources = [
        {
            'name': 'Wikipedia Japanese 10K',
            'url': 'https://raw.githubusercontent.com/hingston/japanese/master/word_frequency/jpn_wikipedia_2021_10K.txt',
            'filename': 'freq_wikipedia_10k.txt'
        },
        {
            'name': 'Japanese Subtitles Frequency',
            'url': 'https://raw.githubusercontent.com/manami-project/anime-offline-database/master/anime-offline-database-minified.json',
            'filename': None  # 이건 다른 용도
        }
    ]
    
    downloaded = []
    
    for source in sources:
        if source['filename'] is None:
            continue
            
        try:
            print(f"Downloading {source['name']}...")
            response = requests.get(source['url'], timeout=30)
            response.raise_for_status()
            
            output_path = os.path.join(OUTPUT_DIR, source['filename'])
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"  Saved to {output_path}")
            downloaded.append(output_path)
        except Exception as e:
            print(f"  Error: {e}")
    
    return downloaded


def parse_frequency_file(filepath: str) -> List[Tuple[str, int]]:
    """빈도수 파일 파싱 (다양한 형식 지원)"""
    
    words_freq = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                # 형식: rank word freq
                try:
                    word = parts[1] if parts[0].isdigit() else parts[0]
                    freq = int(parts[-1]) if parts[-1].isdigit() else len(words_freq) + 1
                    words_freq.append((word, freq))
                except:
                    pass
            elif len(parts) == 1:
                # 단어만 있는 경우
                words_freq.append((parts[0], len(words_freq) + 1))
    
    return words_freq


def get_core_japanese_words() -> List[Dict]:
    """핵심 일본어 단어 목록 생성
    
    JMdict common 단어를 빈도수 순으로 정렬하여
    가장 많이 사용되는 단어 추출
    """
    
    # JMdict common words 로드
    jmdict_file = os.path.join(OUTPUT_DIR, 'jmdict_common_words.json')
    
    if not os.path.exists(jmdict_file):
        print("JMdict common words not found. Run fetch_jlpt_data.py first.")
        return []
    
    with open(jmdict_file, 'r', encoding='utf-8') as f:
        jmdict_words = json.load(f)
    
    print(f"Loaded {len(jmdict_words)} common words from JMdict")
    
    # 빈도수 데이터가 있으면 우선순위 조정
    freq_file = os.path.join(OUTPUT_DIR, 'freq_wikipedia_10k.txt')
    freq_words = set()
    
    if os.path.exists(freq_file):
        with open(freq_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    freq_words.add(parts[1])
        
        print(f"Loaded {len(freq_words)} high-frequency words")
        
        # 빈도 높은 단어 우선 정렬
        high_freq = []
        low_freq = []
        
        for word in jmdict_words:
            word_text = word.get('word', '')
            hiragana = word.get('hiragana', '')
            
            if word_text in freq_words or hiragana in freq_words:
                high_freq.append(word)
            else:
                low_freq.append(word)
        
        print(f"High frequency matches: {len(high_freq)}")
        return high_freq + low_freq
    
    return jmdict_words


def supplement_by_level(existing_data: Dict, target_counts: Dict) -> Dict:
    """레벨별로 목표 단어 수까지 보충"""
    
    # 기존 단어 추출
    existing_words = set()
    for level, words in existing_data.items():
        for word in words:
            existing_words.add(word.get('word', ''))
    
    print(f"Existing unique words: {len(existing_words)}")
    
    # JMdict common 단어 가져오기
    supplement_words = get_core_japanese_words()
    
    if not supplement_words:
        print("No supplement words available")
        return existing_data
    
    # 레벨별 보충
    supplement_index = 0
    
    for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
        current_count = len(existing_data.get(level, []))
        target = target_counts.get(level, 0)
        needed = target - current_count
        
        if needed <= 0:
            print(f"{level}: Already has {current_count} words (target: {target})")
            continue
        
        added = 0
        while added < needed and supplement_index < len(supplement_words):
            word_data = supplement_words[supplement_index]
            supplement_index += 1
            
            word_text = word_data.get('word', '')
            
            if word_text in existing_words:
                continue
            
            existing_words.add(word_text)
            
            if level not in existing_data:
                existing_data[level] = []
            
            existing_data[level].append({
                'word': word_text,
                'kanji': word_data.get('kanji', ''),
                'hiragana': word_data.get('hiragana', ''),
                'romaji': '',
                'definition': word_data.get('definition', ''),
                'partOfSpeech': word_data.get('partOfSpeech', ''),
                'level': level,
                'source': 'JMdict (CC BY-SA 4.0) - Frequency Based'
            })
            added += 1
        
        print(f"{level}: Added {added} words (now: {len(existing_data[level])}, target: {target})")
    
    return existing_data


def main():
    print("="*60)
    print("Frequency-Based Japanese Word Supplement")
    print("="*60)
    
    # 목표 단어 수
    targets = {
        'N5': 800,
        'N4': 1500,
        'N3': 3000,
        'N2': 6000,
        'N1': 10000
    }
    
    print("\nTarget word counts:")
    for level, count in targets.items():
        print(f"  {level}: {count}")
    
    # 빈도수 리스트 다운로드
    print("\n[Step 1] Downloading frequency lists...")
    download_frequency_lists()
    
    # 기존 JLPT 데이터 로드
    print("\n[Step 2] Loading existing JLPT data...")
    combined_file = os.path.join(OUTPUT_DIR, 'combined_jlpt_data.json')
    
    if os.path.exists(combined_file):
        with open(combined_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        print("Loaded existing combined data")
    else:
        # jlpt-vocab-api 데이터만 있는 경우
        api_file = os.path.join(OUTPUT_DIR, 'jlpt_vocab_api.json')
        if os.path.exists(api_file):
            with open(api_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            print("Loaded jlpt-vocab-api data")
        else:
            print("No existing data found. Run fetch_jlpt_data.py first!")
            return
    
    # 현재 상태 출력
    print("\nCurrent word counts:")
    for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
        count = len(existing_data.get(level, []))
        target = targets[level]
        diff = target - count
        status = "✓" if diff <= 0 else f"need +{diff}"
        print(f"  {level}: {count}/{target} ({status})")
    
    # 보충
    print("\n[Step 3] Supplementing words...")
    supplemented_data = supplement_by_level(existing_data, targets)
    
    # 저장
    output_file = os.path.join(OUTPUT_DIR, 'supplemented_jlpt_data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(supplemented_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[Complete] Saved to {output_file}")
    
    # 최종 통계
    print("\nFinal statistics:")
    total = 0
    for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
        count = len(supplemented_data.get(level, []))
        total += count
        print(f"  {level}: {count} words")
    print(f"  Total: {total} unique words")


if __name__ == '__main__':
    main()
