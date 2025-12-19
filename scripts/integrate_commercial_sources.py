#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
상업적 사용 가능한 오픈소스 데이터 통합
- Hanabira JLPT Vocabulary
- Open Anki JLPT Decks
- Tatoeba (선택적)
"""

import json
import os
import requests
import csv
from typing import List, Dict
from collections import defaultdict
from io import StringIO

# 상업적 사용 가능한 데이터 소스
COMMERCIAL_SOURCES = [
    {
        "name": "Open Anki JLPT Decks",
        "license": "MIT",
        "urls": [
            "https://raw.githubusercontent.com/jamsinclair/open-anki-jlpt-decks/main/src/n5.csv",
            "https://raw.githubusercontent.com/jamsinclair/open-anki-jlpt-decks/main/src/n4.csv",
            "https://raw.githubusercontent.com/jamsinclair/open-anki-jlpt-decks/main/src/n3.csv",
            "https://raw.githubusercontent.com/jamsinclair/open-anki-jlpt-decks/main/src/n2.csv",
            "https://raw.githubusercontent.com/jamsinclair/open-anki-jlpt-decks/main/src/n1.csv"
        ],
        "type": "csv",
        "needs_attribution": False
    }
]

TARGET_COUNTS = {
    "N5": 800,
    "N4": 1500,
    "N3": 3000,
    "N2": 6000,
    "N1": 10000
}

def download_file(url: str) -> Dict:
    """파일 다운로드"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return {"success": True, "data": response.text, "content_type": response.headers.get("content-type", "")}
    except Exception as e:
        return {"success": False, "error": str(e)}

def parse_hanabira_json(data: str, level: str) -> List[Dict]:
    """Hanabira JSON 데이터 파싱"""
    words = []
    try:
        json_data = json.loads(data)
        
        # 다양한 구조 처리
        if isinstance(json_data, list):
            items = json_data
        elif isinstance(json_data, dict):
            # 레벨별 키 확인
            if level.lower() in json_data:
                items = json_data[level.lower()]
            elif "words" in json_data:
                items = json_data["words"]
            else:
                items = [json_data]
        else:
            items = []
        
        for item in items:
            if isinstance(item, dict):
                word_text = item.get("word") or item.get("vocab") or item.get("kanji") or item.get("text") or ""
                kanji = item.get("kanji") or item.get("character") or ""
                hiragana = item.get("hiragana") or item.get("reading") or item.get("kana") or item.get("furigana") or ""
                definition = item.get("definition") or item.get("meaning") or item.get("en") or item.get("english") or ""
                
                if word_text or kanji:
                    word = {
                        "word": word_text or kanji,
                        "level": level.upper(),
                        "kanji": kanji or word_text if word_text else "",
                        "hiragana": hiragana,
                        "partOfSpeech": item.get("partOfSpeech") or item.get("pos") or "noun",
                        "definition": definition,
                        "example": item.get("example") or item.get("sentence") or "",
                        "translations": {
                            "en": {
                                "definition": definition,
                                "example": item.get("example") or ""
                            },
                            "ko": {
                                "definition": item.get("ko") or item.get("korean") or "",
                                "example": ""
                            },
                            "zh": {
                                "definition": item.get("zh") or item.get("chinese") or "",
                                "example": ""
                            }
                        },
                        "source": "Hanabira JLPT Vocabulary"
                    }
                    words.append(word)
    except Exception as e:
        print(f"    Error parsing JSON: {e}")
    
    return words

def parse_anki_csv(data: str, level: str) -> List[Dict]:
    """Anki CSV 데이터 파싱"""
    words = []
    try:
        csv_reader = csv.DictReader(StringIO(data))
        
        for row in csv_reader:
            # Anki CSV 구조: expression, reading, meaning, tags, guid
            expression = row.get("expression", "").strip()
            reading = row.get("reading", "").strip()
            meaning = row.get("meaning", "").strip()
            
            if expression:
                # expression이 한자, reading이 히라가나
                word = {
                    "word": expression,
                    "level": level.upper(),
                    "kanji": expression if any(ord(c) > 127 for c in expression) else "",
                    "hiragana": reading if reading else "",
                    "partOfSpeech": "noun",  # 기본값, CSV에 없음
                    "definition": meaning,
                    "example": "",
                    "translations": {
                        "en": {
                            "definition": meaning,
                            "example": ""
                        },
                        "ko": {"definition": "", "example": ""},
                        "zh": {"definition": "", "example": ""}
                    },
                    "source": "Open Anki JLPT Decks"
                }
                words.append(word)
    except Exception as e:
        print(f"    Error parsing CSV: {e}")
        import traceback
        traceback.print_exc()
    
    return words

def integrate_sources() -> Dict[str, List[Dict]]:
    """모든 소스 통합"""
    all_words = defaultdict(list)
    
    for source in COMMERCIAL_SOURCES:
        print(f"\n[{source['name']}]")
        print(f"  License: {source['license']}")
        
        level_map = {
            "n5": "N5",
            "n4": "N4",
            "n3": "N3",
            "n2": "N2",
            "n1": "N1"
        }
        
        for url in source['urls']:
            # 레벨 추출
            level = None
            for key, value in level_map.items():
                if key in url.lower():
                    level = value
                    break
            
            if not level:
                continue
            
            print(f"  Downloading {level}...")
            result = download_file(url)
            
            if result["success"]:
                if source['type'] == "json":
                    words = parse_hanabira_json(result["data"], level)
                elif source['type'] == "csv":
                    words = parse_anki_csv(result["data"], level)
                else:
                    words = []
                
                print(f"    Parsed {len(words)} words")
                all_words[level].extend(words)
            else:
                print(f"    Error: {result.get('error', 'Unknown error')}")
    
    return all_words

def validate_and_deduplicate(all_words: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
    """검증 및 중복 제거"""
    validated = {}
    word_id_start = {
        "N5": 1,
        "N4": 1000,
        "N3": 2000,
        "N2": 3000,
        "N1": 4000
    }
    
    for level in ["N5", "N4", "N3", "N2", "N1"]:
        seen = set()
        unique_words = []
        word_id = word_id_start[level]
        
        for word in all_words[level]:
            word_text = word.get("word", "").strip()
            if not word_text:
                continue
            
            key = (word_text, level)
            if key not in seen:
                word["id"] = word_id
                unique_words.append(word)
                seen.add(key)
                word_id += 1
        
        validated[level] = unique_words
    
    return validated

def save_results(validated_words: Dict[str, List[Dict]]):
    """결과 저장"""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "data")
    os.makedirs(output_dir, exist_ok=True)
    
    # N5-N3 파일
    n5_n3_words = validated_words["N5"] + validated_words["N4"] + validated_words["N3"]
    with open(os.path.join(output_dir, "words_n5_n3.json"), "w", encoding="utf-8") as f:
        json.dump(n5_n3_words, f, ensure_ascii=False, indent=2)
    print(f"[OK] words_n5_n3.json: {len(n5_n3_words)} words")
    
    # N2 파일
    with open(os.path.join(output_dir, "words_n2.json"), "w", encoding="utf-8") as f:
        json.dump(validated_words["N2"], f, ensure_ascii=False, indent=2)
    print(f"[OK] words_n2.json: {len(validated_words['N2'])} words")
    
    # N1 파일
    with open(os.path.join(output_dir, "words_n1.json"), "w", encoding="utf-8") as f:
        json.dump(validated_words["N1"], f, ensure_ascii=False, indent=2)
    print(f"[OK] words_n1.json: {len(validated_words['N1'])} words")

def main():
    """메인 함수"""
    print("=" * 60)
    print("Integrating Commercial-Use Open Source Data")
    print("=" * 60)
    
    # 소스 통합
    all_words = integrate_sources()
    
    # 검증 및 중복 제거
    print("\n" + "=" * 60)
    print("Validating and deduplicating")
    print("=" * 60)
    
    validated_words = validate_and_deduplicate(all_words)
    
    # 결과 출력
    print("\nFinal word counts:")
    total = 0
    for level in ["N5", "N4", "N3", "N2", "N1"]:
        count = len(validated_words[level])
        target = TARGET_COUNTS[level]
        needed = max(0, target - count)
        total += count
        print(f"  {level}: {count}/{target} ({needed} needed)")
    
    # 저장
    print("\n" + "=" * 60)
    print("Saving results")
    print("=" * 60)
    
    save_results(validated_words)
    
    print(f"\nTotal: {total} words")
    print("\n" + "=" * 60)
    print("Data Sources")
    print("=" * 60)
    for source in COMMERCIAL_SOURCES:
        print(f"  - {source['name']}: {source['license']}")
        if source.get('needs_attribution'):
            print(f"    (Attribution required)")

if __name__ == "__main__":
    main()

