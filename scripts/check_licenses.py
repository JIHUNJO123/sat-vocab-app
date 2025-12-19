#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 저장소 라이선스 확인
"""

import requests
import json

def check_license(repo_name):
    """저장소의 라이선스 확인"""
    print(f"\n{'='*60}")
    print(f"Checking license: {repo_name}")
    print(f"{'='*60}")
    
    try:
        # GitHub API로 저장소 정보 확인
        api_url = f"https://api.github.com/repos/{repo_name}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            repo_data = response.json()
            
            # 라이선스 정보
            license_info = repo_data.get("license")
            if license_info:
                license_name = license_info.get("name", "Unknown")
                license_key = license_info.get("key", "unknown")
                license_url = license_info.get("url", "")
                
                print(f"License: {license_name} ({license_key})")
                print(f"License URL: {license_url}")
                
                # 안전한 라이선스 목록
                safe_licenses = [
                    "mit", "apache-2.0", "bsd-3-clause", "bsd-2-clause",
                    "isc", "unlicense", "cc0-1.0", "cc-by-4.0", "cc-by-sa-4.0"
                ]
                
                if license_key.lower() in safe_licenses:
                    print("✅ Safe for commercial use")
                    return True
                else:
                    print("⚠️  License needs review")
                    return False
            else:
                print("⚠️  No license specified")
                return False
        else:
            print(f"Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# 확인할 저장소들
repos = [
    "Bluskyo/JLPT_Vocabulary",
    "AnchorI/jlpt-kanji-dictionary"
]

print("=" * 60)
print("License Check for Repositories")
print("=" * 60)

safe_repos = []
for repo in repos:
    if check_license(repo):
        safe_repos.append(repo)

print(f"\n{'='*60}")
print(f"Safe repositories: {len(safe_repos)}/{len(repos)}")
for repo in safe_repos:
    print(f"  ✅ {repo}")

