#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
추가 데이터 소스 찾기 (목표 달성까지)
"""

import requests
import json
import time

def search_github_extended():
    """확장된 GitHub 검색"""
    queries = [
        "jlpt complete vocabulary",
        "jlpt all levels json",
        "japanese vocabulary complete",
        "jlpt n1 complete list",
        "jlpt dataset"
    ]
    
    found = []
    
    for query in queries:
        try:
            url = "https://api.github.com/search/repositories"
            params = {"q": query, "sort": "stars", "per_page": 20}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                repos = response.json().get("items", [])
                for repo in repos:
                    license_info = repo.get("license")
                    if license_info:
                        license_key = license_info.get("key", "").lower()
                        if license_key in ["mit", "apache-2.0", "bsd-3-clause", "unlicense"]:
                            found.append({
                                "name": repo["full_name"],
                                "license": license_key.upper(),
                                "stars": repo.get("stargazers_count", 0),
                                "url": repo.get("html_url", "")
                            })
            time.sleep(1)
        except:
            pass
    
    # 중복 제거
    unique = {}
    for repo in found:
        if repo["name"] not in unique:
            unique[repo["name"]] = repo
    
    return list(unique.values())

if __name__ == "__main__":
    print("=" * 60)
    print("Finding Additional Sources")
    print("=" * 60)
    
    repos = search_github_extended()
    
    print(f"\nFound {len(repos)} additional repositories:")
    for repo in repos[:10]:
        print(f"  - {repo['name']} ({repo['license']}, {repo['stars']} stars)")

