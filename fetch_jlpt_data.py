"""
JLPT 데이터 수집 스크립트
1. jlpt-vocab-api에서 기본 JLPT 단어 가져오기
2. JMdict-simplified에서 추가 단어 추출
3. 빈도수 기반 일본어 단어 보충

라이선스:
- tanos.co.uk 데이터: CC BY
- JMdict 데이터: CC BY-SA 4.0 (상업적 사용 가능, 저작자 표시 필요)
"""

import json
import requests
import os
import time
from typing import Dict, List, Set, Tuple

# 데이터 저장 경로
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'raw_data')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_jlpt_vocab_api():
    """jlpt-vocab-api에서 기본 JLPT 단어 가져오기"""
    base_url = "https://jlpt-vocab-api.vercel.app/api/words"
    all_words = {}
    
    for level in [5, 4, 3, 2, 1]:
        print(f"Fetching N{level} from jlpt-vocab-api...")
        try:
            # 모든 단어를 가져오기 위해 limit을 크게 설정
            level_words = []
            offset = 0
            limit = 1000
            
            while True:
                response = requests.get(
                    f"{base_url}?level={level}&limit={limit}&offset={offset}", 
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                
                # API 응답 구조: {"total": N, "offset": N, "limit": N, "words": [...]}
                words = data.get('words', [])
                total = data.get('total', 0)
                
                level_words.extend(words)
                
                if len(level_words) >= total or len(words) == 0:
                    break
                
                offset += limit
                time.sleep(0.5)  # Rate limiting
            
            all_words[f"N{level}"] = level_words
            print(f"  N{level}: {len(level_words)} words (total: {total})")
            time.sleep(0.5)
        except Exception as e:
            print(f"  Error fetching N{level}: {e}")
            all_words[f"N{level}"] = []
    
    # 저장
    output_file = os.path.join(OUTPUT_DIR, 'jlpt_vocab_api.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_words, f, ensure_ascii=False, indent=2)
    print(f"Saved to {output_file}")
    
    return all_words


def download_jmdict_simplified():
    """JMdict-simplified JSON 다운로드"""
    print("\nDownloading JMdict-simplified...")
    
    # common-only 버전 (더 작음)
    url = "https://github.com/scriptin/jmdict-simplified/releases/download/3.6.1%2B20251215123412/jmdict-eng-common-3.6.1+20251215123412.json.zip"
    
    output_file = os.path.join(OUTPUT_DIR, 'jmdict-eng-common.json.zip')
    
    print(f"  Downloading from: {url}")
    print(f"  This may take a while (~20MB compressed)...")
    
    try:
        response = requests.get(url, timeout=300, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\r  Progress: {percent:.1f}%", end='')
        
        print(f"\n  Saved to {output_file}")
        
        # 압축 해제
        import zipfile
        print("  Extracting...")
        with zipfile.ZipFile(output_file, 'r') as zip_ref:
            zip_ref.extractall(OUTPUT_DIR)
        print("  Extraction complete!")
        
        return True
    except Exception as e:
        print(f"  Error downloading JMdict: {e}")
        return False


def extract_jlpt_from_jmdict():
    """JMdict에서 JLPT 태그된 단어 추출 (실제로는 misc 태그에 없음)
    대신 common 단어 중 빈도수가 높은 것을 추출"""
    
    jmdict_files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith('jmdict') and f.endswith('.json')]
    
    if not jmdict_files:
        print("JMdict JSON file not found. Download first.")
        return None
    
    jmdict_file = os.path.join(OUTPUT_DIR, jmdict_files[0])
    print(f"\nLoading JMdict from {jmdict_file}...")
    
    with open(jmdict_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    words = data.get('words', [])
    print(f"Total entries in JMdict: {len(words)}")
    
    # common 단어만 추출 (news1, ichi1, spec1, spec2, gai1)
    common_words = []
    
    for entry in words:
        # 가장 일반적인 표기 가져오기
        kanji_list = entry.get('kanji', [])
        kana_list = entry.get('kana', [])
        senses = entry.get('sense', [])
        
        if not kana_list:
            continue
        
        # 첫 번째 가나 표기
        primary_kana = kana_list[0].get('text', '')
        
        # 한자 표기 (있으면)
        primary_kanji = kanji_list[0].get('text', '') if kanji_list else ''
        
        # common 태그 확인
        kanji_common = any(k.get('common', False) for k in kanji_list)
        kana_common = any(k.get('common', False) for k in kana_list)
        
        if not (kanji_common or kana_common):
            continue
        
        # 영어 정의 추출
        definitions = []
        part_of_speech = []
        
        for sense in senses:
            gloss_list = sense.get('gloss', [])
            for gloss in gloss_list:
                if gloss.get('lang', 'eng') == 'eng':
                    definitions.append(gloss.get('text', ''))
            
            pos = sense.get('partOfSpeech', [])
            part_of_speech.extend(pos)
        
        if not definitions:
            continue
        
        word_data = {
            'word': primary_kanji or primary_kana,
            'kanji': primary_kanji,
            'hiragana': primary_kana,
            'definition': '; '.join(definitions[:3]),  # 처음 3개 정의
            'partOfSpeech': part_of_speech[0] if part_of_speech else 'unknown',
            'source': 'JMdict'
        }
        
        common_words.append(word_data)
    
    print(f"Common words extracted: {len(common_words)}")
    
    # 저장
    output_file = os.path.join(OUTPUT_DIR, 'jmdict_common_words.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(common_words, f, ensure_ascii=False, indent=2)
    print(f"Saved to {output_file}")
    
    return common_words


def download_word_frequency():
    """일본어 단어 빈도수 데이터 다운로드"""
    print("\nDownloading word frequency data...")
    
    # Leeds University Japanese Word Frequency List (CC BY)
    # 또는 Wikipedia 빈도수 데이터 사용
    
    # 대안: GitHub의 일본어 빈도수 리스트
    urls = [
        "https://raw.githubusercontent.com/hingston/japanese/master/word_frequency/jpn_wikipedia_2021_10K.txt"
    ]
    
    for url in urls:
        try:
            print(f"  Trying: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            output_file = os.path.join(OUTPUT_DIR, 'word_frequency.txt')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"  Saved to {output_file}")
            return True
        except Exception as e:
            print(f"  Error: {e}")
    
    return False


def fetch_tanos_data():
    """tanos.co.uk에서 직접 JLPT 단어 스크래핑 (CC BY 라이선스)
    
    참고: tanos.co.uk는 직접 스크래핑이 필요하며,
    jlpt-vocab-api가 이미 이 데이터를 제공합니다.
    """
    print("\nNote: tanos.co.uk data is available via jlpt-vocab-api")
    print("License: Creative Commons BY (attribution required)")
    print("Attribution: Jonathan Waller - http://www.tanos.co.uk/jlpt/")


def create_combined_dataset():
    """모든 소스를 결합하여 최종 데이터셋 생성"""
    print("\n" + "="*50)
    print("Creating combined dataset...")
    print("="*50)
    
    # 1. jlpt-vocab-api 데이터 로드
    api_file = os.path.join(OUTPUT_DIR, 'jlpt_vocab_api.json')
    if os.path.exists(api_file):
        with open(api_file, 'r', encoding='utf-8') as f:
            jlpt_data = json.load(f)
    else:
        print("Run fetch_jlpt_vocab_api() first!")
        return
    
    # 기존 단어 목록 (중복 체크용)
    existing_words: Set[str] = set()
    final_data = {'N5': [], 'N4': [], 'N3': [], 'N2': [], 'N1': []}
    
    # JLPT API 데이터 추가
    for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
        for word in jlpt_data.get(level, []):
            word_text = word.get('word', '')
            if word_text and word_text not in existing_words:
                existing_words.add(word_text)
                final_data[level].append({
                    'word': word_text,
                    'kanji': word_text if any('\u4e00' <= c <= '\u9fff' for c in word_text) else '',
                    'hiragana': word.get('furigana', ''),
                    'romaji': word.get('romaji', ''),
                    'definition': word.get('meaning', ''),
                    'partOfSpeech': '',
                    'level': level,
                    'source': 'tanos.co.uk (CC BY)'
                })
    
    print("\nCurrent word counts from jlpt-vocab-api:")
    for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
        print(f"  {level}: {len(final_data[level])} words")
    
    # 2. JMdict common 단어로 보충
    jmdict_file = os.path.join(OUTPUT_DIR, 'jmdict_common_words.json')
    if os.path.exists(jmdict_file):
        with open(jmdict_file, 'r', encoding='utf-8') as f:
            jmdict_words = json.load(f)
        
        # 타겟 단어 수 (중복 제외)
        targets = {'N5': 800, 'N4': 1500, 'N3': 3000, 'N2': 6000, 'N1': 10000}
        
        print("\nSupplementing with JMdict common words...")
        
        # N5부터 순차적으로 보충
        jmdict_index = 0
        for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
            current = len(final_data[level])
            target = targets[level]
            needed = target - current
            
            if needed <= 0:
                continue
            
            added = 0
            while added < needed and jmdict_index < len(jmdict_words):
                word_data = jmdict_words[jmdict_index]
                jmdict_index += 1
                
                word_text = word_data.get('word', '')
                if word_text and word_text not in existing_words:
                    existing_words.add(word_text)
                    
                    final_data[level].append({
                        'word': word_text,
                        'kanji': word_data.get('kanji', ''),
                        'hiragana': word_data.get('hiragana', ''),
                        'romaji': '',
                        'definition': word_data.get('definition', ''),
                        'partOfSpeech': word_data.get('partOfSpeech', ''),
                        'level': level,
                        'source': 'JMdict (CC BY-SA 4.0)'
                    })
                    added += 1
            
            print(f"  {level}: Added {added} words from JMdict")
    
    # 최종 결과 출력
    print("\n" + "="*50)
    print("Final word counts:")
    print("="*50)
    total = 0
    for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
        count = len(final_data[level])
        total += count
        print(f"  {level}: {count} words")
    print(f"  Total: {total} words (no duplicates)")
    
    # 저장
    output_file = os.path.join(OUTPUT_DIR, 'combined_jlpt_data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {output_file}")
    
    return final_data


def main():
    print("="*60)
    print("JLPT Vocabulary Data Collection Script")
    print("="*60)
    print("\nData Sources:")
    print("  1. jlpt-vocab-api (tanos.co.uk) - CC BY license")
    print("  2. JMdict-simplified - CC BY-SA 4.0 license")
    print("  3. Word frequency data - For prioritization")
    print()
    
    # Step 1: jlpt-vocab-api에서 기본 데이터 가져오기
    print("\n[Step 1] Fetching from jlpt-vocab-api...")
    fetch_jlpt_vocab_api()
    
    # Step 2: JMdict 다운로드 (선택적, 대용량)
    print("\n[Step 2] Download JMdict? This is ~20MB compressed.")
    user_input = input("Download JMdict for supplementary data? (y/n): ").strip().lower()
    if user_input == 'y':
        if download_jmdict_simplified():
            extract_jlpt_from_jmdict()
    
    # Step 3: 빈도수 데이터 다운로드 (선택적)
    # download_word_frequency()
    
    # Step 4: 데이터 결합
    print("\n[Step 3] Creating combined dataset...")
    create_combined_dataset()
    
    print("\n" + "="*60)
    print("Data collection complete!")
    print("="*60)
    print(f"\nFiles saved to: {OUTPUT_DIR}")
    print("\nLICENSE REQUIREMENTS:")
    print("  - tanos.co.uk data: Attribution required")
    print("    'JLPT vocabulary from http://www.tanos.co.uk/jlpt/'")
    print("  - JMdict data: Attribution + ShareAlike required")
    print("    See: http://www.edrdg.org/edrdg/licence.html")


if __name__ == '__main__':
    main()
