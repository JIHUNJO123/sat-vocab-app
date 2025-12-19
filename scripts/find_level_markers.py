#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""레벨 마커 찾기"""

import requests
import json

url = "https://raw.githubusercontent.com/FerchusGames/JLPT-Migaku-Progress-Tracker/main/JLPT_Vocab.json"
response = requests.get(url, timeout=60)
data = response.json()

# 레벨 마커 찾기
level_markers = []
for i, item in enumerate(data):
    if isinstance(item, list) and len(item) >= 2:
        item0 = item[0] if isinstance(item[0], str) else str(item[0])
        item1 = item[1] if isinstance(item[1], str) else str(item[1])
        
        if item0 == item1 and item0.upper() in ["N5", "N4", "N3", "N2", "N1"]:
            level_markers.append((i, item0.upper()))

print(f"Found {len(level_markers)} level markers:")
for idx, level in level_markers[:20]:
    print(f"  Index {idx}: {level}")

# 각 레벨 마커 사이의 단어 개수 확인
if len(level_markers) > 1:
    print("\nWords between markers:")
    for i in range(len(level_markers) - 1):
        start_idx = level_markers[i][0]
        end_idx = level_markers[i+1][0]
        count = end_idx - start_idx - 1
        print(f"  {level_markers[i][1]}: {count} words (indices {start_idx+1} to {end_idx-1})")

