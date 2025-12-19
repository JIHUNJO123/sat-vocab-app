#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FerchusGames 데이터 구조 확인"""

import requests
import json

url = "https://raw.githubusercontent.com/FerchusGames/JLPT-Migaku-Progress-Tracker/main/JLPT_Vocab.json"

response = requests.get(url, timeout=30)
data = response.json()

print(f"Total items: {len(data)}")
print(f"Type: {type(data)}")

# 처음 10개 항목 확인
print("\nFirst 10 items:")
for i, item in enumerate(data[:10]):
    print(f"{i+1}: {item}")

# 다양한 길이의 항목 확인
lengths = {}
for item in data[:100]:
    length = len(item) if isinstance(item, (list, dict)) else 0
    lengths[length] = lengths.get(length, 0) + 1

print("\nItem lengths distribution (first 100):")
for length, count in sorted(lengths.items()):
    print(f"  Length {length}: {count} items")

# 샘플 항목 상세 확인
if len(data) > 0:
    sample = data[0]
    print(f"\nSample item type: {type(sample)}")
    if isinstance(sample, list):
        print(f"Sample item length: {len(sample)}")
        print(f"Sample item: {sample}")

