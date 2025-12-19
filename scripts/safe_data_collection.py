#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
저작권 준수 - 안전한 오픈소스 데이터만 수집
- MIT 라이선스: AnchorI/jlpt-kanji-dictionary ✅
- CC BY 2.0: Tatoeba (출처 명시 필요) ✅
- 공개 데이터: JMdict (상업적 사용 가능) ✅
"""

import json
import os
import requests
from typing import List, Dict

# 안전한 저장소만 사용 (라이선스 확인 완료)
SAFE_REPOSITORIES = [
    {
        "name": "AnchorI/jlpt-kanji-dictionary",
        "license": "MIT",
        "url": "https://raw.githubusercontent.com/AnchorI/jlpt-kanji-dictionary/main/jlpt-kanji.json",
        "note": "MIT License - Commercial use allowed"
    }
]

# 목표 단어 수
TARGET_COUNTS = {
    "N5": 800,
    "N4": 1500,
    "N3": 3000,
    "N2": 6000,
    "N1": 10000
}

def download_safe_data(url: str, repo_name: str) -> Dict:
    """안전한 데이터 다운로드"""
    try:
        print(f"  Downloading from {repo_name}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  Error: {e}")
        return None

def parse_anchori_data(data) -> List[Dict]:
    """AnchorI 데이터 파싱 (MIT 라이선스)"""
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
                            "en": {"definition": item.get("description", "").split(".")[0] if item.get("description") else "", "example": ""},
                            "ko": {"definition": "", "example": ""},
                            "zh": {"definition": "", "example": ""}
                        },
                        "source": "AnchorI/jlpt-kanji-dictionary"
                    }
                    words.append(word)
    
    return words

def generate_additional_words(existing_words: List[Dict], target_count: int, level: str) -> List[Dict]:
    """기존 단어를 기반으로 추가 단어 생성 (변형 없이 - 저작권 준수)"""
    # 실제로는 더 많은 오픈소스 데이터를 찾아야 함
    # 여기서는 기존 단어만 반환 (중복 방지)
    return []

def merge_and_deduplicate(all_words: List[Dict], level: str) -> List[Dict]:
    """중복 제거 및 병합"""
    seen = set()
    unique_words = []
    word_id_start = {
        "N5": 1,
        "N4": 1000,
        "N3": 2000,
        "N2": 3000,
        "N1": 4000
    }[level]
    
    word_id = word_id_start
    
    for word in all_words:
        word_text = word.get("word", "").strip()
        if not word_text:
            continue
            
        key = (word_text, level)
        if key not in seen:
            word["id"] = word_id
            word["level"] = level
            unique_words.append(word)
            seen.add(key)
            word_id += 1
    
    return unique_words

def main():
    """메인 함수"""
    print("=" * 60)
    print("Safe Data Collection (Copyright Compliant)")
    print("=" * 60)
    print("\nUsing only verified open-source data:")
    for repo in SAFE_REPOSITORIES:
        print(f"  [OK] {repo['name']} - {repo['license']}")
    
    # 레벨별 단어 수집
    level_words = {level: [] for level in TARGET_COUNTS.keys()}
    
    # 안전한 저장소에서 데이터 다운로드
    for repo in SAFE_REPOSITORIES:
        print(f"\n[{repo['name']}]")
        data = download_safe_data(repo['url'], repo['name'])
        
        if data:
            words = parse_anchori_data(data)
            
            # 레벨별로 분류
            for word in words:
                level = word.get("level", "N5")
                if level in level_words:
                    level_words[level].append(word)
            
            print(f"  Parsed {len(words)} words")
    
    # 현재 수집된 단어 수 확인
    print("\n" + "=" * 60)
    print("Current Word Counts")
    print("=" * 60)
    for level in TARGET_COUNTS.keys():
        current = len(level_words[level])
        target = TARGET_COUNTS[level]
        needed = max(0, target - current)
        print(f"  {level}: {current}/{target} ({needed} needed)")
    
    # 출력 디렉토리
    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "data")
    os.makedirs(output_dir, exist_ok=True)
    
    # 레벨별로 병합 및 저장
    print("\n" + "=" * 60)
    print("Saving Words")
    print("=" * 60)
    
    # N5-N3 파일 생성
    n5_words = merge_and_deduplicate(level_words["N5"], "N5")
    n4_words = merge_and_deduplicate(level_words["N4"], "N4")
    n3_words = merge_and_deduplicate(level_words["N3"], "N3")
    
    n5_n3_words = n5_words + n4_words + n3_words
    
    with open(os.path.join(output_dir, "words_n5_n3.json"), "w", encoding="utf-8") as f:
        json.dump(n5_n3_words, f, ensure_ascii=False, indent=2)
    print(f"[OK] words_n5_n3.json: {len(n5_n3_words)} words")
    
    # N2 파일 생성
    n2_words = merge_and_deduplicate(level_words["N2"], "N2")
    with open(os.path.join(output_dir, "words_n2.json"), "w", encoding="utf-8") as f:
        json.dump(n2_words, f, ensure_ascii=False, indent=2)
    print(f"[OK] words_n2.json: {len(n2_words)} words")
    
    # N1 파일 생성
    n1_words = merge_and_deduplicate(level_words["N1"], "N1")
    with open(os.path.join(output_dir, "words_n1.json"), "w", encoding="utf-8") as f:
        json.dump(n1_words, f, ensure_ascii=False, indent=2)
    print(f"[OK] words_n1.json: {len(n1_words)} words")
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  N5: {len(n5_words)}/{TARGET_COUNTS['N5']} words")
    print(f"  N4: {len(n4_words)}/{TARGET_COUNTS['N4']} words")
    print(f"  N3: {len(n3_words)}/{TARGET_COUNTS['N3']} words")
    print(f"  N2: {len(n2_words)}/{TARGET_COUNTS['N2']} words")
    print(f"  N1: {len(n1_words)}/{TARGET_COUNTS['N1']} words")
    print(f"  Total: {len(n5_n3_words) + len(n2_words) + len(n1_words)} words")
    
    print("\n" + "=" * 60)
    print("[NOTE] More open-source data sources needed")
    print("=" * 60)
    print("To reach target counts, we need additional safe data sources:")
    print("  1. JMdict (EDICT) - Public domain")
    print("  2. Tatoeba - CC BY 2.0 (with attribution)")
    print("  3. Other verified MIT/Apache licensed repositories")

if __name__ == "__main__":
    main()

