#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 오픈소스 프로젝트에서 JLPT 단어 데이터 다운로드 및 통합
"""

import json
import os
import requests
from typing import List, Dict, Set

# GitHub Raw URL 베이스
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"

# 실제로 존재하는 파일들
REPOSITORIES = [
    {
        "name": "Bluskyo/JLPT_Vocabulary",
        "branch": "main",
        "files": [
            "data/results/JLPTWords.json"
        ]
    },
    {
        "name": "AnchorI/jlpt-kanji-dictionary",
        "branch": "main",
        "files": [
            "jlpt-kanji.json"
        ]
    }
]

def download_file(url: str) -> Dict:
    """GitHub에서 JSON 파일 다운로드"""
    try:
        print(f"  Downloading: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"  Error downloading {url}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"  Error parsing JSON from {url}: {e}")
        return None

def parse_bluskyo_data(data: Dict) -> List[Dict]:
    """Bluskyo/JLPT_Vocabulary 데이터 파싱"""
    words = []
    
    # dict 형식인 경우 모든 값들을 확인
    if isinstance(data, dict):
        # 모든 키-값 쌍을 순회
        for key, value in data.items():
            # 값이 리스트인 경우
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        word = {
                            "word": item.get("word") or item.get("vocab") or item.get("text") or key or "",
                            "level": item.get("level") or item.get("jlpt") or "N5",
                            "kanji": item.get("kanji") or "",
                            "hiragana": item.get("hiragana") or item.get("reading") or item.get("kana") or "",
                            "partOfSpeech": item.get("partOfSpeech") or item.get("pos") or "noun",
                            "definition": item.get("definition") or item.get("meaning") or item.get("en") or "",
                            "example": item.get("example") or item.get("sentence") or "",
                        }
                        
                        # 번역 데이터
                        translations = item.get("translations", {})
                        if isinstance(translations, dict):
                            word["translations"] = {
                                "en": {
                                    "definition": translations.get("en", {}).get("definition") or translations.get("en") or word["definition"],
                                    "example": translations.get("en", {}).get("example") or word["example"]
                                },
                                "ko": {
                                    "definition": translations.get("ko", {}).get("definition") or translations.get("ko") or "",
                                    "example": translations.get("ko", {}).get("example") or ""
                                },
                                "zh": {
                                    "definition": translations.get("zh", {}).get("definition") or translations.get("zh") or "",
                                    "example": translations.get("zh", {}).get("example") or ""
                                }
                            }
                        else:
                            word["translations"] = {
                                "en": {"definition": word["definition"], "example": word["example"]},
                                "ko": {"definition": "", "example": ""},
                                "zh": {"definition": "", "example": ""}
                            }
                        
                        if word["word"]:
                            words.append(word)
            # 값이 dict인 경우
            elif isinstance(value, dict):
                word = {
                    "word": value.get("word") or value.get("vocab") or key or "",
                    "level": value.get("level") or value.get("jlpt") or "N5",
                    "kanji": value.get("kanji") or "",
                    "hiragana": value.get("hiragana") or value.get("reading") or value.get("kana") or "",
                    "partOfSpeech": value.get("partOfSpeech") or value.get("pos") or "noun",
                    "definition": value.get("definition") or value.get("meaning") or value.get("en") or "",
                    "example": value.get("example") or value.get("sentence") or "",
                }
                
                word["translations"] = {
                    "en": {"definition": word["definition"], "example": word["example"]},
                    "ko": {"definition": "", "example": ""},
                    "zh": {"definition": "", "example": ""}
                }
                
                if word["word"]:
                    words.append(word)
    
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                word = {
                    "word": item.get("word") or item.get("vocab") or "",
                    "level": item.get("level") or item.get("jlpt") or "N5",
                    "kanji": item.get("kanji") or "",
                    "hiragana": item.get("hiragana") or item.get("reading") or item.get("kana") or "",
                    "partOfSpeech": item.get("partOfSpeech") or item.get("pos") or "noun",
                    "definition": item.get("definition") or item.get("meaning") or item.get("en") or "",
                    "example": item.get("example") or item.get("sentence") or "",
                }
                
                word["translations"] = {
                    "en": {"definition": word["definition"], "example": word["example"]},
                    "ko": {"definition": "", "example": ""},
                    "zh": {"definition": "", "example": ""}
                }
                
                if word["word"]:
                    words.append(word)
    
    return words

def parse_anchori_data(data) -> List[Dict]:
    """AnchorI/jlpt-kanji-dictionary 데이터 파싱 (한자 중심)"""
    words = []
    
    if isinstance(data, list):
        # 리스트 형식 - 각 항목이 한자 정보
        for item in data:
            if isinstance(item, dict):
                # jlpt 필드에서 레벨 추출
                jlpt = item.get("jlpt") or "N5"
                if jlpt and isinstance(jlpt, str):
                    level = jlpt.upper() if jlpt.upper().startswith("N") else f"N{jlpt}"
                else:
                    level = "N5"
                
                kanji = item.get("kanji") or item.get("utf") or ""
                
                # 한자를 단어로 사용 (한자 중심 데이터이므로)
                if kanji:
                    word = {
                        "word": kanji,
                        "level": level,
                        "kanji": kanji,
                        "hiragana": "",  # 한자 데이터에는 히라가나가 없을 수 있음
                        "partOfSpeech": "noun",
                        "definition": item.get("description", "").split(".")[0] if item.get("description") else "",
                        "example": "",
                    }
                    
                    word["translations"] = {
                        "en": {"definition": word["definition"], "example": ""},
                        "ko": {"definition": "", "example": ""},
                        "zh": {"definition": "", "example": ""}
                    }
                    
                    words.append(word)
    
    elif isinstance(data, dict):
        # 딕셔너리 형식
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                # 재귀적으로 처리
                words.extend(parse_anchori_data(value))
    
    return words

def merge_word_lists(all_words: List[Dict], level: str) -> List[Dict]:
    """중복 제거하고 단어 리스트 병합"""
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
        # 중복 체크: (word, level) 조합
        word_text = word.get("word", "").strip()
        if not word_text:
            continue
            
        key = (word_text, level)
        if key not in seen:
            word["id"] = word_id
            # 레벨 명시
            word["level"] = level
            unique_words.append(word)
            seen.add(key)
            word_id += 1
    
    return unique_words

def main():
    """메인 함수"""
    print("=" * 60)
    print("GitHub 오픈소스 프로젝트에서 JLPT 단어 다운로드")
    print("=" * 60)
    
    # 레벨별 단어 수집
    level_words = {
        "N5": [],
        "N4": [],
        "N3": [],
        "N2": [],
        "N1": []
    }
    
    # 각 저장소에서 데이터 다운로드
    for repo in REPOSITORIES:
        repo_name = repo["name"]
        branch = repo.get("branch", "main")
        print(f"\n[{repo_name}]")
        
        for file_path in repo["files"]:
            # URL 구성
            url = f"{GITHUB_RAW_BASE}/{repo_name}/{branch}/{file_path}"
            
            # 다운로드
            data = download_file(url)
            if data:
                # 저장소별 파싱
                if "Bluskyo" in repo_name:
                    words = parse_bluskyo_data(data)
                elif "AnchorI" in repo_name:
                    words = parse_anchori_data(data)
                else:
                    words = []
                
                # 레벨별로 분류
                for word in words:
                    level = word.get("level", "N5").upper()
                    if level in level_words:
                        level_words[level].append(word)
                
                print(f"    Parsed {len(words)} words")
    
    # 출력 디렉토리
    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "data")
    os.makedirs(output_dir, exist_ok=True)
    
    # 레벨별로 병합 및 저장
    print("\n" + "=" * 60)
    print("단어 병합 및 저장")
    print("=" * 60)
    
    # N5-N3 파일 생성
    n5_words = merge_word_lists(level_words["N5"], "N5")
    n4_words = merge_word_lists(level_words["N4"], "N4")
    n3_words = merge_word_lists(level_words["N3"], "N3")
    
    n5_n3_words = n5_words + n4_words + n3_words
    
    with open(os.path.join(output_dir, "words_n5_n3.json"), "w", encoding="utf-8") as f:
        json.dump(n5_n3_words, f, ensure_ascii=False, indent=2)
    print(f"[OK] words_n5_n3.json: {len(n5_n3_words)} words (N5: {len(n5_words)}, N4: {len(n4_words)}, N3: {len(n3_words)})")
    
    # N2 파일 생성
    n2_words = merge_word_lists(level_words["N2"], "N2")
    with open(os.path.join(output_dir, "words_n2.json"), "w", encoding="utf-8") as f:
        json.dump(n2_words, f, ensure_ascii=False, indent=2)
    print(f"[OK] words_n2.json: {len(n2_words)} words")
    
    # N1 파일 생성
    n1_words = merge_word_lists(level_words["N1"], "N1")
    with open(os.path.join(output_dir, "words_n1.json"), "w", encoding="utf-8") as f:
        json.dump(n1_words, f, ensure_ascii=False, indent=2)
    print(f"[OK] words_n1.json: {len(n1_words)} words")
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  N5: {len(n5_words)} words")
    print(f"  N4: {len(n4_words)} words")
    print(f"  N3: {len(n3_words)} words")
    print(f"  N2: {len(n2_words)} words")
    print(f"  N1: {len(n1_words)} words")
    print(f"  Total: {len(n5_n3_words) + len(n2_words) + len(n1_words)} words")

if __name__ == "__main__":
    main()
