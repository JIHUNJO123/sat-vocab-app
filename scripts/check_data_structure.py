#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
다운로드한 데이터 구조 확인
"""

import json
import requests

def check_structure(url, name):
    print(f"\n{'='*60}")
    print(f"Checking: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            
            print(f"Type: {type(data)}")
            
            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())[:10]}")
                if data:
                    first_key = list(data.keys())[0]
                    print(f"First key type: {type(data[first_key])}")
                    if isinstance(data[first_key], (dict, list)):
                        print(f"First key sample: {str(data[first_key])[:200]}")
            elif isinstance(data, list):
                print(f"Length: {len(data)}")
                if data:
                    print(f"First item type: {type(data[0])}")
                    print(f"First item: {json.dumps(data[0], ensure_ascii=False, indent=2)[:500]}")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

# 확인할 파일들
files = [
    ("https://raw.githubusercontent.com/Bluskyo/JLPT_Vocabulary/main/data/results/JLPTWords.json", "Bluskyo/JLPT_Vocabulary"),
    ("https://raw.githubusercontent.com/AnchorI/jlpt-kanji-dictionary/main/jlpt-kanji.json", "AnchorI/jlpt-kanji-dictionary")
]

for url, name in files:
    check_structure(url, name)

