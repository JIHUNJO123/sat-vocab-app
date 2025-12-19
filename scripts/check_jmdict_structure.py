#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JMdict 구조 확인 및 JLPT 레벨 정보 존재 여부 확인
"""

import requests
import xml.etree.ElementTree as ET
from io import BytesIO

def check_jmdict_structure():
    """JMdict XML 구조 확인"""
    print("=" * 60)
    print("Checking JMdict Structure")
    print("=" * 60)
    
    # JMdict 다운로드 URL (작은 샘플 파일로 먼저 확인)
    # 실제로는 전체 파일이 크므로 구조만 확인
    print("\nJMdict 정보:")
    print("  - URL: http://www.edrdg.org/jmdict/j_jmdict.html")
    print("  - Format: XML")
    print("  - Size: ~50MB (압축)")
    print("  - License: CC BY-SA 3.0 / Public Domain")
    
    print("\nJMdict XML 구조:")
    print("  <entry>")
    print("    <k_ele> (한자 정보)")
    print("      <keb> (한자)")
    print("      <ke_inf> (정보)")
    print("    </k_ele>")
    print("    <r_ele> (읽기 정보)")
    print("      <reb> (히라가나/가타카나)")
    print("      <re_inf> (정보)")
    print("    </r_ele>")
    print("    <sense> (의미)")
    print("      <gloss> (번역)")
    print("      <pos> (품사)")
    print("      <field> (분야)")
    print("      <misc> (기타 - 여기에 JLPT 정보가 있을 수 있음)")
    print("    </sense>")
    print("  </entry>")
    
    print("\n" + "=" * 60)
    print("JLPT 레벨 정보 확인 필요")
    print("=" * 60)
    print("JMdict 자체에는 JLPT 레벨 정보가 없을 수 있습니다.")
    print("대안:")
    print("  1. JMdict + 별도 JLPT 레벨 매핑 데이터 사용")
    print("  2. JLPT 빈출 단어 리스트와 매칭")
    print("  3. 기존 JLPT 단어장 데이터와 교차 검증")

def check_alternative_sources():
    """대안 데이터 소스 확인"""
    print("\n" + "=" * 60)
    print("JLPT 전용 데이터 소스")
    print("=" * 60)
    
    sources = [
        {
            "name": "JMdict + JLPT 매핑",
            "description": "JMdict 단어를 JLPT 레벨별 리스트와 매칭",
            "license": "CC BY-SA 3.0",
            "pros": "포괄적, 정확한 번역",
            "cons": "JLPT 레벨 매핑 작업 필요"
        },
        {
            "name": "Tatoeba + JLPT 태그",
            "description": "Tatoeba의 JLPT 태그가 있는 문장",
            "license": "CC BY 2.0",
            "pros": "예문 풍부",
            "cons": "단어 중심이 아닌 문장 중심"
        },
        {
            "name": "기존 JLPT 단어장 데이터",
            "description": "검증된 JLPT 단어장의 단어 리스트",
            "license": "다양함 (확인 필요)",
            "pros": "JLPT 레벨 명확",
            "cons": "저작권 확인 필요"
        }
    ]
    
    for i, source in enumerate(sources, 1):
        print(f"\n{i}. {source['name']}")
        print(f"   설명: {source['description']}")
        print(f"   라이선스: {source['license']}")
        print(f"   장점: {source['pros']}")
        print(f"   단점: {source['cons']}")

if __name__ == "__main__":
    check_jmdict_structure()
    check_alternative_sources()
    
    print("\n" + "=" * 60)
    print("권장 접근 방법")
    print("=" * 60)
    print("1. JMdict에서 단어 추출")
    print("2. 검증된 JLPT 빈출 단어 리스트와 매칭")
    print("3. 매칭된 단어만 사용 (JLPT 관련 단어만)")
    print("4. 기존 AnchorI 데이터와 병합")

