#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FerchusGames 데이터 분석"""

import requests
import json

url = "https://raw.githubusercontent.com/FerchusGames/JLPT-Migaku-Progress-Tracker/main/JLPT_Vocab.json"
response = requests.get(url, timeout=30)
data = response.json()

print(f"Total items: {len(data)}")

# 레벨별 개수 확인
level_counts = {}
current_level = "N5"

for item in data:
    if isinstance(item, list) and len(item) >= 2:
        # 레벨 표시 확인
        if item[0] == item[1] and isinstance(item[0], str) and item[0].upper().startswith("N"):
            current_level = item[0].upper()
        # 단어 데이터
        elif len(item) == 2 and isinstance(item[0], str):
            level_counts[current_level] = level_counts.get(current_level, 0) + 1

print("\nLevel distribution:")
for level in ["N5", "N4", "N3", "N2", "N1"]:
    count = level_counts.get(level, 0)
    print(f"  {level}: {count} words")

total = sum(level_counts.values())
print(f"\nTotal words: {total}")

