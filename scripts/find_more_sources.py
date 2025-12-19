#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
더 많은 상업적 사용 가능한 JLPT 데이터 소스 찾기
"""

import requests
import json
import time

def search_github_repos(query, max_results=30):
    """GitHub 저장소 검색"""
    url = "https://api.github.com/search/repositories"
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
        return []
    except:
        return []

def check_license_and_structure(repo):
    """라이선스 및 구조 확인"""
    repo_name = repo["full_name"]
    license_info = repo.get("license")
    license_key = license_info.get("key", "").lower() if license_info else None
    
    # 안전한 라이선스
    safe_licenses = ["mit", "apache-2.0", "bsd-3-clause", "bsd-2-clause", "isc", "unlicense"]
    
    if license_key not in safe_licenses:
        return None
    
    # 저장소 구조 확인
    try:
        url = f"https://api.github.com/repos/{repo_name}/git/trees/main?recursive=1"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            url = f"https://api.github.com/repos/{repo_name}/git/trees/master?recursive=1"
            response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            files = [item["path"] for item in data.get("tree", []) if item["type"] == "blob"]
            
            # JLPT 관련 파일 찾기
            jlpt_files = [f for f in files if any(level in f.lower() for level in ['n5', 'n4', 'n3', 'n2', 'n1', 'jlpt'])]
            
            if jlpt_files:
                return {
                    "name": repo_name,
                    "license": license_key.upper(),
                    "stars": repo.get("stargazers_count", 0),
                    "files": jlpt_files[:10],
                    "url": repo.get("html_url", "")
                }
    except:
        pass
    
    return None

def main():
    """메인 함수"""
    print("=" * 60)
    print("Finding More Commercial-Use JLPT Data Sources")
    print("=" * 60)
    
    search_queries = [
        "jlpt vocabulary",
        "jlpt vocab json",
        "jlpt word list",
        "jlpt n1 n2 n3",
        "japanese vocabulary jlpt"
    ]
    
    found_repos = []
    
    for query in search_queries:
        print(f"\nSearching: {query}")
        repos = search_github_repos(query, max_results=30)
        
        for repo in repos:
            result = check_license_and_structure(repo)
            if result:
                found_repos.append(result)
                print(f"  [FOUND] {result['name']} ({result['license']})")
        
        time.sleep(1)  # API rate limit 방지
    
    # 중복 제거
    unique_repos = {}
    for repo in found_repos:
        if repo["name"] not in unique_repos:
            unique_repos[repo["name"]] = repo
    
    print("\n" + "=" * 60)
    print(f"Found {len(unique_repos)} verified repositories")
    print("=" * 60)
    
    for repo in unique_repos.values():
        print(f"\n{repo['name']}")
        print(f"  License: {repo['license']}")
        print(f"  Stars: {repo['stars']}")
        print(f"  Files: {', '.join(repo['files'][:3])}")
        print(f"  URL: {repo['url']}")
    
    return list(unique_repos.values())

if __name__ == "__main__":
    repos = main()

