#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FerchusGames 전체 파싱 테스트"""

import requests
import json

url = "https://raw.githubusercontent.com/FerchusGames/JLPT-Migaku-Progress-Tracker/main/JLPT_Vocab.json"
response = requests.get(url, timeout=60)
data = response.json()

print(f"Total items: {len(data)}")

# 레벨 마커 찾기
level_markers = []
for idx, item in enumerate(data):
    if isinstance(item, list) and len(item) >= 2:
        item0 = item[0] if isinstance(item[0], str) else str(item[0])
        item1 = item[1] if isinstance(item[1], str) else str(item[1])
        if item0 == item1 and item0.upper() in ["N5", "N4", "N3", "N2", "N1"]:
            level_markers.append((idx, item0.upper()))

print(f"\nLevel markers: {len(level_markers)}")
for idx, level in level_markers:
    print(f"  {level} at index {idx}")

# 각 레벨별 단어 파싱
words_by_level = {}
for i in range(len(level_markers)):
    start_idx = level_markers[i][0] + 1
    end_idx = level_markers[i+1][0] if i+1 < len(level_markers) else len(data)
    level = level_markers[i][1]
    
    words = []
    for idx in range(start_idx, end_idx):
        item = data[idx]
        if isinstance(item, list) and len(item) >= 2:
            item0 = item[0] if isinstance(item[0], str) else str(item[0])
            item1 = item[1] if isinstance(item[1], str) else str(item[1])
            if item0.strip():
                words.append(item0.strip())
    
    words_by_level[level] = words
    print(f"\n{level}: {len(words)} words (indices {start_idx} to {end_idx-1})")

print("\nTotal words parsed:")
total = 0
for level in ["N5", "N4", "N3", "N2", "N1"]:
    count = len(words_by_level.get(level, []))
    total += count
    print(f"  {level}: {count} words")

print(f"\nGrand total: {total} words")

