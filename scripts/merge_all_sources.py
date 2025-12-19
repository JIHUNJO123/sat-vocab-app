#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 검증된 소스 통합
- AnchorI/jlpt-kanji-dictionary (MIT)
- Open Anki JLPT Decks (MIT)
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
    """AnchorI 데이터 다운로드"""
    print("\n[AnchorI/jlpt-kanji-dictionary]")
    print("  License: MIT")
    
    try:
        response = requests.get(ALL_SOURCES[0]["url"], timeout=30)
        response.raise_for_status()
        data = response.json()
        
        words = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    jlpt = item.get("jlpt") or "N5"
                    if jlpt and isinstance(jlpt, str):
                        level = jlpt.upper() if jlpt.upper().startswith("N") else f"N{jlpt}"
                    else:
                        level = "N5"
                    
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
                                "en": {
                                    "definition": item.get("description", "").split(".")[0] if item.get("description") else "",
                                    "example": ""
                                },
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

def download_anki(level: str) -> List[Dict]:
    """Anki CSV 데이터 다운로드"""
    url = ALL_SOURCES[1]["urls"].get(level)
    if not url:
        return []
    
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
        
        return words
    except Exception as e:
        print(f"  Error downloading {level}: {e}")
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
    print("Merging All Verified Sources")
    print("=" * 60)
    
    all_words = defaultdict(list)
    
    # AnchorI 데이터
    anchori_words = download_anchori()
    for word in anchori_words:
        level = word.get("level", "N5")
        if level in all_words:
            all_words[level].append(word)
    
    # Anki 데이터
    print("\n[Open Anki JLPT Decks]")
    print("  License: MIT")
    for level in ["N5", "N4", "N3", "N2", "N1"]:
        print(f"  Downloading {level}...")
        anki_words = download_anki(level)
        all_words[level].extend(anki_words)
        print(f"    {len(anki_words)} words")
    
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
        print(f"  {level}: {count}/{target} ({percentage:.1f}%, {needed} needed)")
    
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
    print("  - AnchorI/jlpt-kanji-dictionary")
    print("  - Open Anki JLPT Decks")
    print("\nAll sources are MIT licensed - commercial use allowed!")

if __name__ == "__main__":
    main()

