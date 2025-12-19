# JLPT 단어 추가 방법 가이드

## 방법 1: 공개 오픈소스 데이터셋 활용 (추천 ⭐⭐⭐⭐⭐)

### 장점:
- ✅ 무료
- ✅ 저작권 문제 없음 (오픈소스)
- ✅ 이미 검증된 데이터
- ✅ 빠른 구현

### 추천 소스:

1. **Tatoeba Project**
   - URL: https://tatoeba.org/
   - 다국어 문장 데이터베이스
   - CC BY 2.0 라이선스
   - 일본어 문장과 번역 포함

2. **JMdict (Japanese-Multilingual Dictionary)**
   - URL: http://www.edrdg.org/jmdict/j_jmdict.html
   - 가장 포괄적인 일본어 사전 데이터
   - 무료 사용 가능
   - 다국어 번역 포함

3. **KanjiDict**
   - 한자와 단어 데이터
   - 오픈소스

4. **GitHub 오픈소스 프로젝트**
   - 검색어: "jlpt vocabulary json github"
   - 예: https://github.com/search?q=jlpt+vocabulary+json

### 구현 방법:
```python
# 예시: GitHub에서 JSON 데이터 다운로드
import requests
import json

url = "https://raw.githubusercontent.com/[repo]/[path]/jlpt_words.json"
response = requests.get(url)
data = response.json()
# 데이터 변환 및 통합
```

---

## 방법 2: 웹 스크래핑 (주의 필요 ⚠️)

### 장점:
- ✅ 많은 데이터 소스
- ✅ 최신 정보

### 단점:
- ⚠️ 저작권 문제 가능
- ⚠️ 웹사이트 정책 위반 가능
- ⚠️ 법적 리스크

### 주의사항:
- robots.txt 확인 필수
- 저작권 확인 필수
- 개인/상업적 사용 여부 확인

### 추천 사이트 (공개 데이터):
- **JLPT Study Guide** (공개 데이터)
- **Tae Kim's Guide** (일부 공개)

---

## 방법 3: Google Translate API / 번역 API 활용 (비용 발생 💰)

### 장점:
- ✅ 빠른 번역
- ✅ 다국어 지원
- ✅ 일관된 품질

### 단점:
- ❌ 비용 발생 (월 $20 무료 크레딧 후 유료)
- ❌ API 키 관리 필요
- ❌ 번역 품질이 완벽하지 않을 수 있음

### 비용:
- Google Cloud Translation API: $20/100만자
- DeepL API: 더 비싸지만 품질 좋음

### 구현 예시:
```python
from google.cloud import translate_v2 as translate

def translate_text(text, target_language='ko'):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']
```

---

## 방법 4: AI 도구 활용 (ChatGPT, Claude 등) (비용 발생 💰)

### 장점:
- ✅ 빠른 생성
- ✅ 컨텍스트 이해
- ✅ 일관된 형식

### 단점:
- ❌ 비용 발생
- ❌ 정확도 검증 필요
- ❌ 대량 생성 시 비용 증가

### 구현 방법:
- ChatGPT API로 단어 리스트 생성 요청
- 배치 처리로 대량 생성

---

## 방법 5: 기존 앱/사이트 데이터 활용 (주의 필요 ⚠️)

### 주의사항:
- ⚠️ 저작권 확인 필수
- ⚠️ 개인 사용 vs 상업적 사용 구분
- ⚠️ 데이터 출처 명시 필요

---

## 방법 6: 하이브리드 접근법 (추천 ⭐⭐⭐⭐)

### 단계별 전략:

1. **1단계: 공개 데이터셋 수집**
   - JMdict 다운로드
   - GitHub 오픈소스 프로젝트 활용
   - 무료 데이터 우선 수집

2. **2단계: 데이터 정제 및 변환**
   - 형식 통일
   - 중복 제거
   - 레벨 분류

3. **3단계: 부족한 부분만 API로 보완**
   - 특정 레벨 단어 부족 시
   - 번역이 없는 경우만 API 사용
   - 비용 최소화

4. **4단계: 검증**
   - 수동 검토
   - 사용자 피드백 반영

---

## 추천 구현 순서

### 즉시 실행 가능 (무료):

1. **JMdict 다운로드 및 파싱**
   ```bash
   # JMdict XML 다운로드
   wget http://www.edrdg.org/jmdict/j_jmdict.html
   # XML 파싱하여 JSON 변환
   ```

2. **GitHub 오픈소스 프로젝트 검색**
   - "jlpt vocabulary" 검색
   - JSON 형식 데이터 다운로드
   - 직접 통합

3. **Tatoeba 데이터 활용**
   - 일본어-영어 문장 쌍
   - 예문으로 활용

### 비용 발생하지만 효율적:

4. **Google Translate API (선택적)**
   - 부족한 번역만 보완
   - 월 $20 무료 크레딧 활용
   - 비용 최소화

---

## 예상 비용

### 무료 방법:
- JMdict: 무료
- GitHub 오픈소스: 무료
- Tatoeba: 무료
- **총 비용: $0**

### API 활용 시:
- Google Translate: 월 $20 무료 크레딧 (100만자)
- 부족한 번역만 보완: 약 $10-50
- **총 비용: $10-50 (일회성)**

---

## 최종 추천

### 🏆 **1순위: 공개 데이터셋 활용 (무료)**
- JMdict + GitHub 오픈소스
- 빠르고 무료
- 저작권 문제 없음

### 🥈 **2순위: 하이브리드 접근**
- 공개 데이터 + 선택적 API 보완
- 비용 최소화하면서 품질 확보

### 🥉 **3순위: API 전면 활용**
- 빠르지만 비용 발생
- 대량 생성 시 비용 증가

---

## 다음 단계

원하시는 방법을 선택해주시면 구체적인 구현 코드를 제공하겠습니다:
1. JMdict 파싱 스크립트 작성
2. GitHub 오픈소스 데이터 통합
3. Google Translate API 통합 (선택적)

