#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
실제 저장소 구조 확인 및 올바른 URL 찾기
"""

import requests
import json

def check_repo_structure(repo_name, branch="main"):
    """저장소 구조 확인"""
    print(f"\n{'='*60}")
    print(f"Checking: {repo_name}")
    print(f"{'='*60}")
    
    # GitHub API로 저장소 내용 확인
    url = f"https://api.github.com/repos/{repo_name}/git/trees/{branch}?recursive=1"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            # master 브랜치 시도
            url = f"https://api.github.com/repos/{repo_name}/git/trees/master?recursive=1"
            response = requests.get(url, timeout=10)
            branch = "master"
        
        if response.status_code == 200:
            data = response.json()
            files = [item["path"] for item in data.get("tree", []) if item["type"] == "blob"]
            
            # JSON/CSV 파일 찾기
            json_files = [f for f in files if f.endswith('.json')]
            csv_files = [f for f in files if f.endswith('.csv')]
            
            # JLPT 관련 파일
            jlpt_json = [f for f in json_files if any(level in f.lower() for level in ['n5', 'n4', 'n3', 'n2', 'n1', 'jlpt'])]
            jlpt_csv = [f for f in csv_files if any(level in f.lower() for level in ['n5', 'n4', 'n3', 'n2', 'n1', 'jlpt'])]
            
            print(f"JSON files: {len(json_files)}")
            print(f"CSV files: {len(csv_files)}")
            print(f"JLPT JSON files: {len(jlpt_json)}")
            print(f"JLPT CSV files: {len(jlpt_csv)}")
            
            if jlpt_json:
                print(f"\nJLPT JSON files found:")
                for f in jlpt_json[:10]:
                    print(f"  - {f}")
            
            if jlpt_csv:
                print(f"\nJLPT CSV files found:")
                for f in jlpt_csv[:10]:
                    print(f"  - {f}")
            
            return {
                "branch": branch,
                "jlpt_json": jlpt_json,
                "jlpt_csv": jlpt_csv
            }
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# 확인할 저장소들
repos_to_check = [
    "hanabira/jlpt-vocab",
    "jamsinclair/open-anki-jlpt-decks"
]

print("=" * 60)
print("Finding Actual Repository Structures")
print("=" * 60)

for repo in repos_to_check:
    result = check_repo_structure(repo)
    if result:
        print(f"\n{repo} structure:")
        print(f"  Branch: {result['branch']}")
        print(f"  JLPT files: {len(result['jlpt_json']) + len(result['jlpt_csv'])}")

