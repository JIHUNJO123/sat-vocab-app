#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FerchusGames 파싱 테스트"""

import requests
import json

url = "https://raw.githubusercontent.com/FerchusGames/JLPT-Migaku-Progress-Tracker/main/JLPT_Vocab.json"
response = requests.get(url, timeout=60)
data = response.json()

print(f"Total items: {len(data)}")

words = []
current_level = "N5"

for i, item in enumerate(data):
    if isinstance(item, list) and len(item) >= 2:
        item0 = item[0] if isinstance(item[0], str) else str(item[0])
        item1 = item[1] if isinstance(item[1], str) else str(item[1])
        
        # 레벨 표시 확인
        if item0 == item1 and item0.upper() in ["N5", "N4", "N3", "N2", "N1"]:
            current_level = item0.upper()
            if i < 100:
                print(f"Level change to {current_level} at index {i}")
        # 단어 데이터
        elif item0 != item1:
            if item0.strip() and item0.upper() not in ["N5", "N4", "N3", "N2", "N1"]:
                words.append({
                    "word": item0.strip(),
                    "hiragana": item1.strip(),
                    "level": current_level
                })

print(f"\nTotal words parsed: {len(words)}")

# 레벨별 개수
level_counts = {}
for word in words:
    level = word["level"]
    level_counts[level] = level_counts.get(level, 0) + 1

print("\nLevel distribution:")
for level in ["N5", "N4", "N3", "N2", "N1"]:
    print(f"  {level}: {level_counts.get(level, 0)} words")

