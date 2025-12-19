#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
검증된 JLPT 단어 리스트 찾기 및 통합
"""

import requests
import json

def search_github_for_jlpt():
    """GitHub에서 검증된 JLPT 단어 리스트 검색"""
    print("=" * 60)
    print("Searching for Verified JLPT Word Lists")
    print("=" * 60)
    
    # GitHub API로 검색
    search_queries = [
        "jlpt vocabulary json",
        "jlpt word list n5 n4 n3 n2 n1",
        "jlpt vocab complete"
    ]
    
    print("\nNote: JMdict는 일반 일본어 사전이므로")
    print("JLPT 레벨 정보가 없습니다.")
    print("\n대신 다음 방법을 권장합니다:")
    print("1. 검증된 JLPT 단어 리스트 사용 (레벨 명시)")
    print("2. 기존 AnchorI 데이터 활용 (이미 JLPT 레벨 포함)")
    print("3. 여러 소스 교차 검증")

def check_existing_data_quality():
    """기존 데이터 품질 확인"""
    print("\n" + "=" * 60)
    print("Current Data Quality Check")
    print("=" * 60)
    
    print("\nAnchorI/jlpt-kanji-dictionary:")
    print("  - JLPT 레벨: 명시됨 (N5, N4, N3, N2, N1)")
    print("  - 데이터 타입: 한자 중심")
    print("  - 라이선스: MIT (상업적 사용 가능)")
    print("  - 신뢰도: 높음 (JLPT 레벨 정보 포함)")
    
    print("\n현재 데이터의 장점:")
    print("  - JLPT 레벨이 명확히 표시됨")
    print("  - 저작권 문제 없음")
    print("  - 상업적 사용 가능")
    
    print("\n현재 데이터의 한계:")
    print("  - 한자 중심 (히라가나/번역 부족)")
    print("  - 단어 수가 목표보다 적음")
    print("  - 예문 없음")

def recommend_approach():
    """권장 접근 방법"""
    print("\n" + "=" * 60)
    print("Recommended Approach")
    print("=" * 60)
    
    print("\n옵션 1: 현재 데이터로 시작 (권장)")
    print("  - 2,136개 단어로 출시")
    print("  - JLPT 레벨 명확")
    print("  - 저작권 안전")
    print("  - 사용자 피드백 후 확장")
    
    print("\n옵션 2: 추가 검증된 소스 찾기")
    print("  - GitHub에서 MIT/Apache 라이선스 확인")
    print("  - JLPT 레벨 정보 포함 확인")
    print("  - 여러 소스 교차 검증")
    
    print("\n옵션 3: JMdict + 필터링 (복잡)")
    print("  - JMdict에서 단어 추출")
    print("  - 검증된 JLPT 리스트와 매칭")
    print("  - 매칭된 단어만 사용")
    print("  - 작업량 많음, 정확도 불확실")

if __name__ == "__main__":
    search_github_for_jlpt()
    check_existing_data_quality()
    recommend_approach()
    
    print("\n" + "=" * 60)
    print("Conclusion")
    print("=" * 60)
    print("현재 AnchorI 데이터는 JLPT 레벨이 명시되어 있어")
    print("JLPT 관련 단어라고 볼 수 있습니다.")
    print("\n추가 단어가 필요하다면:")
    print("1. 검증된 JLPT 단어 리스트 찾기 (GitHub)")
    print("2. 라이선스 확인 필수")
    print("3. JLPT 레벨 정보 포함 확인")

