#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json

url = "https://raw.githubusercontent.com/FerchusGames/JLPT-Migaku-Progress-Tracker/main/JLPT_Vocab.json"
response = requests.get(url, timeout=30)
data = response.json()

# 파일로 저장
with open("ferchus_sample.json", "w", encoding="utf-8") as f:
    json.dump(data[:100], f, ensure_ascii=False, indent=2)

print(f"Total: {len(data)} items")
print(f"First item: {data[0]}")
print(f"Second item: {data[1] if len(data) > 1 else 'N/A'}")
print(f"Third item: {data[2] if len(data) > 2 else 'N/A'}")

# 레벨별 개수 확인
level_counts = {}
for item in data[:1000]:  # 처음 1000개만 확인
    if isinstance(item, list) and len(item) >= 2:
        level = item[0] if isinstance(item[0], str) else str(item[0])
        level_counts[level] = level_counts.get(level, 0) + 1

print("\nLevel distribution (first 1000 items):")
for level, count in sorted(level_counts.items()):
    print(f"  {level}: {count}")

