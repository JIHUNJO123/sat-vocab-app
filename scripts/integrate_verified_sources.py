#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
검증된 소스 통합 및 교차 검증
"""

import json
import os
import requests
from typing import List, Dict, Set
from collections import defaultdict

# 검증된 저장소 목록 (라이선스 확인 완료)
VERIFIED_REPOS = [
    {
        "name": "AnchorI/jlpt-kanji-dictionary",
        "license": "MIT",
        "url": "https://raw.githubusercontent.com/AnchorI/jlpt-kanji-dictionary/main/jlpt-kanji.json",
        "type": "kanji"
    },
    {
        "name": "Bluskyo/JLPT_Vocabulary",
        "license": "Unknown - needs verification",
        "url": "https://raw.githubusercontent.com/Bluskyo/JLPT_Vocabulary/main/data/results/JLPTWords.json",
        "type": "vocabulary",
        "status": "checking"
    }
]

TARGET_COUNTS = {
    "N5": 800,
    "N4": 1500,
    "N3": 3000,
    "N2": 6000,
    "N1": 10000
}

def download_data(url: str, repo_name: str) -> Dict:
    """데이터 다운로드"""
    try:
        print(f"  Downloading from {repo_name}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  Error: {e}")
        return None

def parse_anchori_data(data) -> List[Dict]:
    """AnchorI 데이터 파싱"""
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

def parse_bluskyo_data(data: Dict) -> List[Dict]:
    """Bluskyo 데이터 파싱 (구조 확인 필요)"""
    words = []
    
    # 다양한 구조 시도
    if isinstance(data, dict):
        # 딕셔너리의 모든 값 확인
        for key, value in data.items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        level = item.get("level") or item.get("jlpt") or "N5"
                        if isinstance(level, str):
                            level = level.upper() if level.upper().startswith("N") else f"N{level}"
                        else:
                            level = "N5"
                        
                        word_text = item.get("word") or item.get("vocab") or item.get("text") or key or ""
                        
                        if word_text:
                            word = {
                                "word": word_text,
                                "level": level,
                                "kanji": item.get("kanji") or "",
                                "hiragana": item.get("hiragana") or item.get("reading") or item.get("kana") or "",
                                "partOfSpeech": item.get("partOfSpeech") or item.get("pos") or "noun",
                                "definition": item.get("definition") or item.get("meaning") or item.get("en") or "",
                                "example": item.get("example") or item.get("sentence") or "",
                                "translations": {
                                    "en": {"definition": item.get("definition") or "", "example": item.get("example") or ""},
                                    "ko": {"definition": item.get("ko") or "", "example": ""},
                                    "zh": {"definition": item.get("zh") or "", "example": ""}
                                },
                                "source": "Bluskyo/JLPT_Vocabulary"
                            }
                            words.append(word)
            elif isinstance(value, dict):
                # 중첩 딕셔너리
                words.extend(parse_bluskyo_data(value))
    
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                level = item.get("level") or item.get("jlpt") or "N5"
                if isinstance(level, str):
                    level = level.upper() if level.upper().startswith("N") else f"N{level}"
                else:
                    level = "N5"
                
                word_text = item.get("word") or item.get("vocab") or ""
                
                if word_text:
                    word = {
                        "word": word_text,
                        "level": level,
                        "kanji": item.get("kanji") or "",
                        "hiragana": item.get("hiragana") or item.get("reading") or "",
                        "partOfSpeech": item.get("partOfSpeech") or "noun",
                        "definition": item.get("definition") or "",
                        "example": item.get("example") or "",
                        "translations": {
                            "en": {"definition": item.get("definition") or "", "example": ""},
                            "ko": {"definition": "", "example": ""},
                            "zh": {"definition": "", "example": ""}
                        },
                        "source": "Bluskyo/JLPT_Vocabulary"
                    }
                    words.append(word)
    
    return words

def cross_validate_words(all_words: List[Dict]) -> Dict[str, List[Dict]]:
    """여러 소스의 단어 교차 검증"""
    # 레벨별로 그룹화
    level_words = defaultdict(list)
    
    for word in all_words:
        level = word.get("level", "N5")
        if level in ["N5", "N4", "N3", "N2", "N1"]:
            level_words[level].append(word)
    
    # 중복 제거 (같은 단어, 같은 레벨)
    validated = {}
    for level in ["N5", "N4", "N3", "N2", "N1"]:
        seen = set()
        unique_words = []
        
        for word in level_words[level]:
            word_text = word.get("word", "").strip()
            if not word_text:
                continue
            
            key = (word_text, level)
            if key not in seen:
                unique_words.append(word)
                seen.add(key)
        
        validated[level] = unique_words
    
    return validated

def merge_and_save(validated_words: Dict[str, List[Dict]]):
    """병합 및 저장"""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "data")
    os.makedirs(output_dir, exist_ok=True)
    
    # ID 할당
    word_id_start = {
        "N5": 1,
        "N4": 1000,
        "N3": 2000,
        "N2": 3000,
        "N1": 4000
    }
    
    for level in ["N5", "N4", "N3", "N2", "N1"]:
        word_id = word_id_start[level]
        for word in validated_words[level]:
            word["id"] = word_id
            word_id += 1
    
    # N5-N3 파일 생성
    n5_n3_words = validated_words["N5"] + validated_words["N4"] + validated_words["N3"]
    
    with open(os.path.join(output_dir, "words_n5_n3.json"), "w", encoding="utf-8") as f:
        json.dump(n5_n3_words, f, ensure_ascii=False, indent=2)
    print(f"[OK] words_n5_n3.json: {len(n5_n3_words)} words")
    
    # N2 파일 생성
    with open(os.path.join(output_dir, "words_n2.json"), "w", encoding="utf-8") as f:
        json.dump(validated_words["N2"], f, ensure_ascii=False, indent=2)
    print(f"[OK] words_n2.json: {len(validated_words['N2'])} words")
    
    # N1 파일 생성
    with open(os.path.join(output_dir, "words_n1.json"), "w", encoding="utf-8") as f:
        json.dump(validated_words["N1"], f, ensure_ascii=False, indent=2)
    print(f"[OK] words_n1.json: {len(validated_words['N1'])} words")

def main():
    """메인 함수"""
    print("=" * 60)
    print("Integrating Verified Sources")
    print("=" * 60)
    
    all_words = []
    
    # 각 저장소에서 데이터 수집
    for repo in VERIFIED_REPOS:
        if repo.get("status") == "checking":
            print(f"\n[{repo['name']}] - Checking license...")
            continue
        
        print(f"\n[{repo['name']}]")
        print(f"  License: {repo['license']}")
        
        data = download_data(repo['url'], repo['name'])
        if data:
            if "AnchorI" in repo['name']:
                words = parse_anchori_data(data)
            elif "Bluskyo" in repo['name']:
                words = parse_bluskyo_data(data)
            else:
                words = []
            
            print(f"  Parsed {len(words)} words")
            all_words.extend(words)
    
    # 교차 검증
    print("\n" + "=" * 60)
    print("Cross-validating words")
    print("=" * 60)
    
    validated_words = cross_validate_words(all_words)
    
    # 결과 출력
    print("\nValidated word counts:")
    for level in ["N5", "N4", "N3", "N2", "N1"]:
        count = len(validated_words[level])
        target = TARGET_COUNTS[level]
        print(f"  {level}: {count}/{target} ({target - count} needed)")
    
    # 저장
    print("\n" + "=" * 60)
    print("Saving validated words")
    print("=" * 60)
    
    merge_and_save(validated_words)
    
    total = sum(len(validated_words[level]) for level in ["N5", "N4", "N3", "N2", "N1"])
    print(f"\nTotal: {total} validated words")

if __name__ == "__main__":
    main()

