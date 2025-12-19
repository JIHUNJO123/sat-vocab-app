# GitHub Pages URL 문제 해결

## 현재 상태
✅ 파일들이 저장소 루트의 `docs` 폴더에 올바르게 업로드되었습니다.

## 확인 사항

### 1. GitHub Pages 설정 확인
1. https://github.com/JIHUNJO123/jlpt-step-apps/settings/pages 로 이동
2. 다음 설정 확인:
   - **Source**: `Deploy from a branch` 선택
   - **Branch**: `main` 선택
   - **Folder**: `/docs` 선택
   - **Save** 클릭

### 2. 저장소 공개 여부 확인
- 저장소가 **Public**이어야 GitHub Pages가 작동합니다
- Private 저장소는 GitHub Pro가 필요합니다

### 3. 활성화 대기
- 설정 후 **1-5분** 정도 기다려야 합니다
- Pages 탭에서 "Your site is live at..." 메시지가 나타나면 활성화된 것입니다

### 4. 올바른 URL 형식
저장소 이름이 `jlpt-step-apps`이고 사용자명이 `JIHUNJO123`이면:

**올바른 URL:**
- https://jihunjo123.github.io/jlpt-step-apps/privacy-policy-n5-n3.html
- https://jihunjo123.github.io/jlpt-step-apps/marketing-n5-n3.html
- https://jihunjo123.github.io/jlpt-step-apps/support-n5-n3.html

**잘못된 URL (404 발생):**
- https://jihunjo123.github.io/jlpt-step-apps/docs/privacy-policy-n5-n3.html ❌
  (URL에 `/docs`를 포함하면 안 됩니다!)

### 5. 직접 확인 방법
GitHub 웹에서:
1. https://github.com/JIHUNJO123/jlpt-step-apps 로 이동
2. `docs` 폴더 클릭
3. `privacy-policy-n5-n3.html` 파일이 보이는지 확인
4. 파일을 클릭하면 내용이 보여야 합니다

### 6. Pages 상태 확인
1. Settings > Pages로 이동
2. "Your site is live at..." 메시지 확인
3. 빌드 상태가 "Success"인지 확인

## 여전히 404가 뜬다면
1. 저장소가 Public인지 확인
2. 브랜치 이름이 정확히 `main`인지 확인 (대소문자 구분)
3. `/docs` 폴더 선택이 맞는지 확인
4. 5-10분 더 기다린 후 다시 시도
5. 브라우저 캐시 삭제 후 다시 시도

