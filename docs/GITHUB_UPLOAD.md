# GitHub Pages 업로드 가이드

## 저장소: https://github.com/JIHUNJO123/jlpt-step-apps

## 업로드할 파일 목록

`docs` 폴더의 다음 파일들을 GitHub 저장소의 `docs` 폴더에 업로드하세요:

### JLPT Step N5–N3
- `privacy-policy-n5-n3.html`
- `marketing-n5-n3.html`
- `support-n5-n3.html`

### JLPT Step N2
- `privacy-policy-n2.html`
- `marketing-n2.html`
- `support-n2.html`

### JLPT Step N1
- `privacy-policy-n1.html`
- `marketing-n1.html`
- `support-n1.html`

## GitHub Pages 설정

1. 저장소 Settings > Pages로 이동
2. Source: `main` 브랜치의 `/docs` 폴더 선택
3. Save 클릭

## URL (설정 후 사용 가능)

**JLPT Step N5–N3:**
- Privacy Policy: `https://jihunjo123.github.io/jlpt-step-apps/privacy-policy-n5-n3.html`
- Marketing: `https://jihunjo123.github.io/jlpt-step-apps/marketing-n5-n3.html`
- Support: `https://jihunjo123.github.io/jlpt-step-apps/support-n5-n3.html`

**JLPT Step N2:**
- Privacy Policy: `https://jihunjo123.github.io/jlpt-step-apps/privacy-policy-n2.html`
- Marketing: `https://jihunjo123.github.io/jlpt-step-apps/marketing-n2.html`
- Support: `https://jihunjo123.github.io/jlpt-step-apps/support-n2.html`

**JLPT Step N1:**
- Privacy Policy: `https://jihunjo123.github.io/jlpt-step-apps/privacy-policy-n1.html`
- Marketing: `https://jihunjo123.github.io/jlpt-step-apps/marketing-n1.html`
- Support: `https://jihunjo123.github.io/jlpt-step-apps/support-n1.html`

## 업로드 방법

### 방법 1: GitHub 웹 인터페이스
1. 저장소 페이지에서 `docs` 폴더 클릭 (없으면 생성)
2. "Add file" > "Upload files" 클릭
3. 위 파일들을 드래그 앤 드롭
4. Commit changes

### 방법 2: Git 명령어
```bash
cd C:\Users\hooni\Desktop\jlpt_vocab_app\docs
git init
git add .
git commit -m "Add privacy policy, marketing, and support pages"
git remote add origin https://github.com/JIHUNJO123/jlpt-step-apps.git
git branch -M main
git push -u origin main
```

