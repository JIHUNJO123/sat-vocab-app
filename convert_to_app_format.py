"""
JLPT 앱용 최종 데이터 변환 스크립트

수집한 JLPT 데이터를 앱에서 사용할 수 있는 형식으로 변환합니다.

출력 형식:
- words_n5_n3.json: N5, N4, N3 단어 (무료 버전)
- words_n2.json: N2 단어 (프리미엄)
- words_n1.json: N1 단어 (프리미엄)
"""

import json
import os
from typing import Dict, List


RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), 'raw_data')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'data')


def convert_to_app_format(word: Dict, word_id: int) -> Dict:
    """단어를 앱 형식으로 변환"""
    
    # 영어 정의
    definition = word.get('definition', '') or word.get('meaning', '')
    
    # 품사 정리
    pos = word.get('partOfSpeech', '')
    if isinstance(pos, list):
        pos = pos[0] if pos else 'unknown'
    
    # 품사 약어 변환
    pos_mapping = {
        'noun': 'noun',
        'verb': 'verb',
        'adjective': 'adjective',
        'adverb': 'adverb',
        'i-adjective': 'i-adjective',
        'na-adjective': 'na-adjective',
        'n': 'noun',
        'v': 'verb',
        'adj': 'adjective',
        'adv': 'adverb',
        '': 'unknown'
    }
    pos = pos_mapping.get(pos.lower() if pos else '', pos)
    
    return {
        'id': word_id,
        'word': word.get('word', ''),
        'level': word.get('level', 'N5'),
        'kanji': word.get('kanji', ''),
        'hiragana': word.get('hiragana', '') or word.get('furigana', ''),
        'partOfSpeech': pos,
        'definition': definition,
        'example': word.get('example', ''),
        'translations': {
            'en': {
                'definition': definition,
                'example': word.get('example', '')
            },
            'ko': {
                'definition': '',  # 번역 필요
                'example': ''
            },
            'zh': {
                'definition': '',  # 번역 필요
                'example': ''
            }
        },
        'source': word.get('source', 'tanos.co.uk (CC BY)')
    }


def process_data():
    """데이터 처리 및 변환"""
    
    # 보충된 데이터 로드
    data_file = os.path.join(RAW_DATA_DIR, 'supplemented_jlpt_data.json')
    
    if not os.path.exists(data_file):
        # 대안: combined 또는 api 데이터
        data_file = os.path.join(RAW_DATA_DIR, 'combined_jlpt_data.json')
        if not os.path.exists(data_file):
            data_file = os.path.join(RAW_DATA_DIR, 'jlpt_vocab_api.json')
    
    if not os.path.exists(data_file):
        print(f"No data file found. Run fetch_jlpt_data.py first!")
        return
    
    print(f"Loading data from {data_file}...")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # 레벨별 처리
    n5_n3_words = []
    n2_words = []
    n1_words = []
    
    word_id = 1
    
    for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
        level_words = raw_data.get(level, [])
        print(f"\nProcessing {level}: {len(level_words)} words")
        
        for word in level_words:
            word['level'] = level
            converted = convert_to_app_format(word, word_id)
            word_id += 1
            
            if level in ['N5', 'N4', 'N3']:
                n5_n3_words.append(converted)
            elif level == 'N2':
                n2_words.append(converted)
            else:  # N1
                n1_words.append(converted)
    
    # 출력 디렉토리 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 파일 저장
    files_to_save = [
        ('words_n5_n3.json', n5_n3_words),
        ('words_n2.json', n2_words),
        ('words_n1.json', n1_words),
        ('words.json', n5_n3_words[:1000])  # 기본 파일 (샘플)
    ]
    
    for filename, words in files_to_save:
        output_path = os.path.join(OUTPUT_DIR, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(words, f, ensure_ascii=False, indent=2)
        print(f"Saved {filename}: {len(words)} words")
    
    # 통계 출력
    print("\n" + "="*50)
    print("Final Statistics")
    print("="*50)
    print(f"N5-N3 (Free): {len(n5_n3_words)} words")
    print(f"N2 (Premium): {len(n2_words)} words")
    print(f"N1 (Premium): {len(n1_words)} words")
    print(f"Total: {len(n5_n3_words) + len(n2_words) + len(n1_words)} words")
    
    # 라이선스 정보 파일 생성
    license_info = """
JLPT Vocabulary Data Attribution
================================

This application uses vocabulary data from the following sources:

1. JLPT Vocabulary Lists by Jonathan Waller
   - Website: http://www.tanos.co.uk/jlpt/
   - License: Creative Commons Attribution (CC BY)
   - Attribution: "JLPT vocabulary from http://www.tanos.co.uk/jlpt/"

2. JMdict Dictionary Data
   - Project: Electronic Dictionary Research and Development Group
   - Website: http://www.edrdg.org/jmdict/j_jmdict.html
   - License: Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)
   - License URL: http://www.edrdg.org/edrdg/licence.html
   - Attribution: "This application uses the JMdict dictionary file.
     These files are the property of the Electronic Dictionary Research
     and Development Group, and are used in conformance with the Group's licence."

Note: When using CC BY-SA licensed content, any derivative works must also
be shared under the same or compatible license terms.

For questions about licensing, please contact the original data providers.
"""
    
    license_path = os.path.join(OUTPUT_DIR, 'LICENSE_ATTRIBUTION.txt')
    with open(license_path, 'w', encoding='utf-8') as f:
        f.write(license_info)
    print(f"\nLicense attribution saved to {license_path}")


def main():
    print("="*60)
    print("Convert JLPT Data to App Format")
    print("="*60)
    
    process_data()
    
    print("\n" + "="*60)
    print("Conversion Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review the generated JSON files in assets/data/")
    print("2. Add Korean/Chinese translations if needed")
    print("3. Ensure LICENSE_ATTRIBUTION.txt is included in the app")


if __name__ == '__main__':
    main()
