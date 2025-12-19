#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 저장소 구조 탐색 및 파일 경로 확인
"""

import requests
import json

def explore_repo(repo_name, branch="main"):
    """GitHub 저장소 구조 탐색"""
    print(f"\n{'='*60}")
    print(f"Exploring: {repo_name}")
    print(f"{'='*60}")
    
    # GitHub API로 저장소 내용 확인
    api_url = f"https://api.github.com/repos/{repo_name}/git/trees/{branch}?recursive=1"
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            files = [item["path"] for item in data.get("tree", []) if item["type"] == "blob"]
            
            # JSON 파일 찾기
            json_files = [f for f in files if f.endswith('.json')]
            
            print(f"Found {len(json_files)} JSON files:")
            for f in json_files[:20]:  # 처음 20개만 표시
                print(f"  - {f}")
            
            # JLPT 관련 파일 찾기
            jlpt_files = [f for f in json_files if any(level in f.lower() for level in ['n5', 'n4', 'n3', 'n2', 'n1', 'jlpt'])]
            if jlpt_files:
                print(f"\nJLPT related files ({len(jlpt_files)}):")
                for f in jlpt_files:
                    print(f"  - {f}")
            
            return json_files, jlpt_files
        else:
            # main 브랜치가 없으면 master 시도
            if branch == "main":
                return explore_repo(repo_name, "master")
            else:
                print(f"Error: {response.status_code}")
                return [], []
    except Exception as e:
        print(f"Error: {e}")
        return [], []

# 저장소 목록
repos = [
    "Bluskyo/JLPT_Vocabulary",
    "AnchorI/jlpt-kanji-dictionary",
    "mokemokechicken/japanese-word-frequency",
    "ScriptSmith/jlpt-vocab",
    "jamesprior/jlpt-vocab"
]

all_jlpt_files = {}

for repo in repos:
    json_files, jlpt_files = explore_repo(repo)
    if jlpt_files:
        all_jlpt_files[repo] = jlpt_files

print(f"\n{'='*60}")
print("Summary - Repositories with JLPT files:")
print(f"{'='*60}")
for repo, files in all_jlpt_files.items():
    print(f"\n{repo}:")
    for f in files:
        print(f"  {f}")

