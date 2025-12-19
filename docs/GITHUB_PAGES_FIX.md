# GitHub Pages 404 오류 해결 방법

## 문제
파일을 업로드했지만 404 에러가 발생합니다.

## 해결 방법

### 방법 1: 저장소 루트에 파일 복사 (권장)

GitHub Pages가 `/docs` 폴더를 Source로 설정했을 때, 파일 경로는:
- 저장소: `https://github.com/JIHUNJO123/jlpt-step-apps`
- 파일 위치: 저장소 루트의 `docs/` 폴더
- 접근 URL: `https://jihunjo123.github.io/jlpt-step-apps/privacy-policy-n5-n3.html`

현재 파일이 `docs` 폴더 안의 Git 저장소에 있어서 문제가 발생할 수 있습니다.

### 방법 2: 저장소 루트에서 직접 관리

1. GitHub 웹에서 저장소로 이동
2. `docs` 폴더 생성 (없으면)
3. 파일들을 직접 업로드:
   - privacy-policy-n5-n3.html
   - privacy-policy-n2.html
   - privacy-policy-n1.html
   - marketing-n5-n3.html
   - marketing-n2.html
   - marketing-n1.html
   - support-n5-n3.html
   - support-n2.html
   - support-n1.html

### 방법 3: Git으로 저장소 루트에 푸시

```bash
# 저장소 루트로 이동
cd C:\Users\hooni\Desktop
git clone https://github.com/JIHUNJO123/jlpt-step-apps.git
cd jlpt-step-apps

# docs 폴더 생성 및 파일 복사
mkdir docs
copy C:\Users\hooni\Desktop\jlpt_vocab_app\docs\privacy-policy-*.html docs\
copy C:\Users\hooni\Desktop\jlpt_vocab_app\docs\marketing-*.html docs\
copy C:\Users\hooni\Desktop\jlpt_vocab_app\docs\support-*.html docs\

# 커밋 및 푸시
git add docs/
git commit -m "Add privacy policy, marketing, and support pages"
git push origin main
```

## 확인 사항

1. GitHub 저장소에서 `docs` 폴더가 있는지 확인
2. `docs` 폴더 안에 HTML 파일들이 있는지 확인
3. Settings > Pages에서 Source가 `/docs`로 설정되어 있는지 확인
4. Pages가 활성화되기까지 몇 분 걸릴 수 있음

## 예상 URL (설정 후)

- https://jihunjo123.github.io/jlpt-step-apps/privacy-policy-n5-n3.html
- https://jihunjo123.github.io/jlpt-step-apps/marketing-n5-n3.html
- https://jihunjo123.github.io/jlpt-step-apps/support-n5-n3.html

