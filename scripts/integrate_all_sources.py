#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 검증된 소스 통합 (목표 개수까지)
"""

import json
import os
import requests
import csv
from typing import List, Dict
from collections import defaultdict
from io import StringIO

# 모든 검증된 소스
ALL_SOURCES = [
    {
        "name": "AnchorI/jlpt-kanji-dictionary",
        "license": "MIT",
        "url": "https://raw.githubusercontent.com/AnchorI/jlpt-kanji-dictionary/main/jlpt-kanji.json",
        "type": "json"
    },
    {
        "name": "Open Anki JLPT Decks",
        "license": "MIT",
        "urls": {
            "N5": "https://raw.githubusercontent.com/jamsinclair/open-anki-jlpt-decks/main/src/n5.csv",
            "N4": "https://raw.githubusercontent.com/jamsinclair/open-anki-jlpt-decks/main/src/n4.csv",
            "N3": "https://raw.githubusercontent.com/jamsinclair/open-anki-jlpt-decks/main/src/n3.csv",
            "N2": "https://raw.githubusercontent.com/jamsinclair/open-anki-jlpt-decks/main/src/n2.csv",
            "N1": "https://raw.githubusercontent.com/jamsinclair/open-anki-jlpt-decks/main/src/n1.csv"
        },
        "type": "csv"
    },
    {
        "name": "mikan-sour/jlpt_api",
        "license": "MIT",
        "urls": {
            "N5": "https://raw.githubusercontent.com/mikan-sour/jlpt_api/main/dictionaryService/src/dataload/jlptData/jlpt_n5.csv",
            "N4": "https://raw.githubusercontent.com/mikan-sour/jlpt_api/main/dictionaryService/src/dataload/jlptData/jlpt_n4.csv",
            "N3": "https://raw.githubusercontent.com/mikan-sour/jlpt_api/main/dictionaryService/src/dataload/jlptData/jlpt_n3.csv",
            "N2": "https://raw.githubusercontent.com/mikan-sour/jlpt_api/main/dictionaryService/src/dataload/jlptData/jlpt_n2.csv",
            "N1": "https://raw.githubusercontent.com/mikan-sour/jlpt_api/main/dictionaryService/src/dataload/jlptData/jlpt_n1.csv"
        },
        "type": "csv"
    },
    {
        "name": "FerchusGames/JLPT-Migaku-Progress-Tracker",
        "license": "MIT",
        "url": "https://raw.githubusercontent.com/FerchusGames/JLPT-Migaku-Progress-Tracker/main/JLPT_Vocab.json",
        "type": "json"
    }
]

TARGET_COUNTS = {
    "N5": 800,
    "N4": 1500,
    "N3": 3000,
    "N2": 6000,
    "N1": 10000
}

def download_anchori() -> List[Dict]:
    """AnchorI 데이터"""
    print("\n[AnchorI/jlpt-kanji-dictionary]")
    try:
        response = requests.get(ALL_SOURCES[0]["url"], timeout=30)
        response.raise_for_status()
        data = response.json()
        
        words = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    jlpt = item.get("jlpt") or "N5"
                    level = jlpt.upper() if isinstance(jlpt, str) and jlpt.upper().startswith("N") else f"N{jlpt}" if jlpt else "N5"
                    kanji = item.get("kanji") or item.get("utf") or ""
                    
                    if kanji:
                        word = {
                            "word": kanji,
                            "level": level,
                            "kanji": kanji,
                            "hiragana": "",
                            "partOfSpeech": "noun",
                            "definition": item.get("description", "").split(".")[0] if item.get("description") else "",
                            "example": "",
                            "translations": {
                                "en": {"definition": item.get("description", "").split(".")[0] if item.get("description") else "", "example": ""},
                                "ko": {"definition": "", "example": ""},
                                "zh": {"definition": "", "example": ""}
                            },
                            "source": "AnchorI/jlpt-kanji-dictionary"
                        }
                        words.append(word)
        
        print(f"  Parsed {len(words)} words")
        return words
    except Exception as e:
        print(f"  Error: {e}")
        return []

def download_anki_csv(url: str, level: str) -> List[Dict]:
    """Anki 형식 CSV 다운로드"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        words = []
        csv_reader = csv.DictReader(StringIO(response.text))
        
        for row in csv_reader:
            expression = row.get("expression", "").strip()
            reading = row.get("reading", "").strip()
            meaning = row.get("meaning", "").strip()
            
            if expression:
                word = {
                    "word": expression,
                    "level": level.upper(),
                    "kanji": expression if any(ord(c) > 127 for c in expression) else "",
                    "hiragana": reading if reading else "",
                    "partOfSpeech": "noun",
                    "definition": meaning,
                    "example": "",
                    "translations": {
                        "en": {"definition": meaning, "example": ""},
                        "ko": {"definition": "", "example": ""},
                        "zh": {"definition": "", "example": ""}
                    },
                    "source": "Open Anki JLPT Decks"
                }
                words.append(word)
        
        return words
    except Exception as e:
        return []

def download_mikan_csv(url: str, level: str) -> List[Dict]:
    """Mikan 형식 CSV 다운로드 (현재 404 - 스킵)"""
    # mikan-sour 저장소의 파일 경로가 정확하지 않아 스킵
    return []

def download_ferchus_json() -> List[Dict]:
    """FerchusGames JSON 데이터 (33,216개 단어)"""
    print("\n[FerchusGames/JLPT-Migaku-Progress-Tracker]")
    try:
        response = requests.get(ALL_SOURCES[3]["url"], timeout=60)
        response.raise_for_status()
        data = response.json()
        
        words = []
        current_level = "N5"
        
        # 구조: ["N5", "N5"] 다음에 ["会う", "あう"] 형식의 단어들
        # 레벨 마커 위치: 0(N5), 1500(N4), 5001(N3), 15001(N2), 30001(N1)
        if isinstance(data, list):
            # 먼저 레벨 마커 위치 찾기
            level_markers = []
            for idx, item in enumerate(data):
                if isinstance(item, list) and len(item) >= 2:
                    item0_str = item[0] if isinstance(item[0], str) else str(item[0])
                    item1_str = item[1] if isinstance(item[1], str) else str(item[1])
                    if (item0_str == item1_str and 
                        item0_str.upper() in ["N5", "N4", "N3", "N2", "N1"]):
                        level_markers.append((idx, item0_str.upper()))
            
            # 레벨 마커 사이의 모든 항목을 단어로 처리
            for i in range(len(level_markers)):
                start_idx = level_markers[i][0] + 1  # 마커 다음부터
                end_idx = level_markers[i+1][0] if i+1 < len(level_markers) else len(data)
                current_level = level_markers[i][1]
                
                for idx in range(start_idx, end_idx):
                    item = data[idx]
                    if isinstance(item, list) and len(item) >= 2:
                        item0_str = item[0] if isinstance(item[0], str) else str(item[0])
                        item1_str = item[1] if isinstance(item[1], str) else str(item[1])
                        
                        word_text = item0_str.strip()
                        hiragana = item1_str.strip()
                        
                        if word_text:
                            word = {
                                "word": word_text,
                                "level": current_level,
                                "kanji": word_text if any(ord(c) > 127 for c in word_text) else "",
                                "hiragana": hiragana if hiragana else "",
                                "partOfSpeech": "noun",
                                "definition": "",
                                "example": "",
                                "translations": {
                                    "en": {"definition": "", "example": ""},
                                    "ko": {"definition": "", "example": ""},
                                    "zh": {"definition": "", "example": ""}
                                },
                                "source": "FerchusGames/JLPT-Migaku-Progress-Tracker"
                            }
                            words.append(word)
        
        # 레벨별 개수 확인
        level_counts = {}
        for word in words:
            level = word["level"]
            level_counts[level] = level_counts.get(level, 0) + 1
        
        print(f"  Parsed {len(words)} words")
        print(f"  Level distribution:")
        for level in ["N5", "N4", "N3", "N2", "N1"]:
            print(f"    {level}: {level_counts.get(level, 0)} words")
        
        return words
    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        return []

def merge_and_deduplicate(all_words: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
    """병합 및 중복 제거"""
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

def main():
    """메인 함수"""
    print("=" * 60)
    print("Integrating ALL Verified Sources (Target Counts)")
    print("=" * 60)
    
    all_words = defaultdict(list)
    
    # AnchorI 데이터
    anchori_words = download_anchori()
    for word in anchori_words:
        level = word.get("level", "N5")
        if level in ["N5", "N4", "N3", "N2", "N1"]:
            all_words[level].append(word)
    
    # Open Anki JLPT Decks
    print("\n[Open Anki JLPT Decks]")
    for level in ["N5", "N4", "N3", "N2", "N1"]:
        url = ALL_SOURCES[1]["urls"].get(level)
        if url:
            words = download_anki_csv(url, level)
            all_words[level].extend(words)
            print(f"  {level}: {len(words)} words")
    
    # Mikan JLPT API
    print("\n[mikan-sour/jlpt_api]")
    for level in ["N5", "N4", "N3", "N2", "N1"]:
        url = ALL_SOURCES[2]["urls"].get(level)
        if url:
            words = download_mikan_csv(url, level)
            all_words[level].extend(words)
            print(f"  {level}: {len(words)} words")
    
    # FerchusGames JSON
    ferchus_words = download_ferchus_json()
    for word in ferchus_words:
        level = word.get("level", "N5")
        if level in ["N5", "N4", "N3", "N2", "N1"]:
            all_words[level].append(word)
    
    # 병합 및 중복 제거
    print("\n" + "=" * 60)
    print("Merging and deduplicating")
    print("=" * 60)
    
    validated_words = merge_and_deduplicate(all_words)
    
    # 결과 출력
    print("\nFinal word counts:")
    total = 0
    for level in ["N5", "N4", "N3", "N2", "N1"]:
        count = len(validated_words[level])
        target = TARGET_COUNTS[level]
        needed = max(0, target - count)
        percentage = (count / target * 100) if target > 0 else 0
        total += count
        status = "OK" if count >= target else "NEED MORE"
        print(f"  {level}: {count}/{target} ({percentage:.1f}%, {needed} needed) [{status}]")
    
    # 저장
    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "data")
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "=" * 60)
    print("Saving results")
    print("=" * 60)
    
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
    
    print(f"\nTotal: {total} words")
    print("\n" + "=" * 60)
    print("Data Sources (All MIT License)")
    print("=" * 60)
    for source in ALL_SOURCES:
        print(f"  - {source['name']}: {source['license']}")

if __name__ == "__main__":
    main()

