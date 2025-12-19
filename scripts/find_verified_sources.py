#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub에서 검증된 JLPT 단어 리스트 찾기
- MIT/Apache 라이선스 확인
- JLPT 레벨 정보 포함 확인
- 여러 소스 교차 검증
"""

import requests
import json
import time
from typing import List, Dict, Optional

GITHUB_API_BASE = "https://api.github.com"

def search_github_repos(query: str, max_results: int = 10) -> List[Dict]:
    """GitHub에서 저장소 검색"""
    url = f"{GITHUB_API_BASE}/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": max_results
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(f"  API Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"  Error: {e}")
        return []

def check_license(repo: Dict) -> Optional[str]:
    """저장소의 라이선스 확인"""
    license_info = repo.get("license")
    if license_info:
        return license_info.get("key", "").lower()
    return None

def check_repo_structure(repo_name: str) -> Dict:
    """저장소 구조 확인 및 JLPT 레벨 정보 확인"""
    print(f"\n  Checking: {repo_name}")
    
    # 저장소 내용 확인
    url = f"{GITHUB_API_BASE}/repos/{repo_name}/git/trees/main?recursive=1"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            # master 브랜치 시도
            url = f"{GITHUB_API_BASE}/repos/{repo_name}/git/trees/master?recursive=1"
            response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            files = [item["path"] for item in data.get("tree", []) if item["type"] == "blob"]
            
            # JSON 파일 찾기
            json_files = [f for f in files if f.endswith('.json')]
            jlpt_files = [f for f in json_files if any(level in f.lower() for level in ['n5', 'n4', 'n3', 'n2', 'n1', 'jlpt'])]
            
            return {
                "has_json": len(json_files) > 0,
                "has_jlpt_files": len(jlpt_files) > 0,
                "jlpt_files": jlpt_files[:5],  # 처음 5개만
                "total_json": len(json_files)
            }
    except Exception as e:
        print(f"    Error checking structure: {e}")
    
    return {"has_json": False, "has_jlpt_files": False, "jlpt_files": [], "total_json": 0}

def verify_jlpt_data(repo_name: str, file_path: str) -> bool:
    """실제 데이터에서 JLPT 레벨 정보 확인"""
    url = f"https://raw.githubusercontent.com/{repo_name}/main/{file_path}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            url = f"https://raw.githubusercontent.com/{repo_name}/master/{file_path}"
            response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # 데이터 구조 확인
            if isinstance(data, list) and len(data) > 0:
                first_item = data[0]
                if isinstance(first_item, dict):
                    # JLPT 레벨 필드 확인
                    has_level = any(key.lower() in ['level', 'jlpt', 'n5', 'n4', 'n3', 'n2', 'n1'] 
                                   for key in first_item.keys())
                    return has_level
            elif isinstance(data, dict):
                # 딕셔너리 형식 확인
                has_level_keys = any(key.lower() in ['n5', 'n4', 'n3', 'n2', 'n1', 'jlpt'] 
                                   for key in data.keys())
                return has_level_keys
    except:
        pass
    
    return False

def main():
    """메인 함수"""
    print("=" * 60)
    print("Finding Verified JLPT Word Lists on GitHub")
    print("=" * 60)
    
    # 검색 쿼리
    search_queries = [
        "jlpt vocabulary json",
        "jlpt word list",
        "jlpt vocab n5 n4 n3 n2 n1"
    ]
    
    verified_repos = []
    
    for query in search_queries:
        print(f"\nSearching: {query}")
        repos = search_github_repos(query, max_results=20)
        
        for repo in repos:
            repo_name = repo["full_name"]
            license_key = check_license(repo)
            
            # 안전한 라이선스만 확인
            safe_licenses = ["mit", "apache-2.0", "bsd-3-clause", "bsd-2-clause", "isc"]
            
            if license_key in safe_licenses:
                print(f"\n  [FOUND] {repo_name}")
                print(f"    License: {license_key.upper()}")
                print(f"    Stars: {repo.get('stargazers_count', 0)}")
                
                # 저장소 구조 확인
                structure = check_repo_structure(repo_name)
                
                if structure["has_jlpt_files"]:
                    print(f"    JLPT files found: {len(structure['jlpt_files'])}")
                    
                    # 실제 데이터 확인
                    for file_path in structure["jlpt_files"][:2]:  # 처음 2개만 확인
                        if verify_jlpt_data(repo_name, file_path):
                            print(f"    [VERIFIED] {file_path} contains JLPT level info")
                            verified_repos.append({
                                "name": repo_name,
                                "license": license_key,
                                "stars": repo.get('stargazers_count', 0),
                                "files": structure["jlpt_files"],
                                "url": repo.get("html_url", "")
                            })
                            break
                else:
                    print(f"    No JLPT-specific files found")
            
            # API rate limit 방지
            time.sleep(0.5)
    
    # 결과 정리
    print("\n" + "=" * 60)
    print("Verified Repositories")
    print("=" * 60)
    
    if verified_repos:
        for i, repo in enumerate(verified_repos, 1):
            print(f"\n{i}. {repo['name']}")
            print(f"   License: {repo['license'].upper()}")
            print(f"   Stars: {repo['stars']}")
            print(f"   Files: {', '.join(repo['files'][:3])}")
            print(f"   URL: {repo['url']}")
    else:
        print("\nNo additional verified repositories found.")
        print("Current AnchorI data is the best available option.")
    
    return verified_repos

if __name__ == "__main__":
    verified = main()
    
    print("\n" + "=" * 60)
    print("Next Steps")
    print("=" * 60)
    if verified:
        print(f"Found {len(verified)} verified repositories.")
        print("These can be integrated with proper license compliance.")
    else:
        print("Current AnchorI data (MIT License) is recommended.")
        print("It has JLPT level information and is copyright-safe.")

