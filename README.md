# parkseongjin.me

Gavin Park의 개발 블로그. [parkseongjin.me](https://parkseongjin.me)

## 스택

- [Astro](https://astro.build) — 정적 사이트 생성기
- GitHub Pages — 호스팅
- GitHub Actions — `main`에 push하면 자동 빌드·배포

## 새 글 쓰기

`src/content/blog/` 에 마크다운(`.md`) 또는 MDX(`.mdx`) 파일을 추가합니다.

```markdown
---
title: '글 제목'
description: '목록과 SEO에 쓰이는 한 줄 요약'
pubDate: 'Sep 24 2026'
heroImage: '../../assets/blog-placeholder-1.jpg'  # 선택
---

본문...
```

커밋하고 push하면 몇 분 안에 사이트에 반영됩니다.

## 로컬 개발

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # dist/ 로 정적 빌드
npm run preview  # 빌드 결과 미리보기
```

## 구조

| 경로 | 용도 |
|---|---|
| `src/content/blog/` | 글 (마크다운) |
| `src/pages/` | 페이지 (홈, about, 글 목록, RSS) |
| `src/components/` | 헤더·푸터 등 컴포넌트 |
| `src/layouts/` | 글 레이아웃 |
| `src/consts.ts` | 사이트 제목·설명 |
| `public/` | 정적 파일 (favicon, CNAME) |
| `.github/workflows/deploy.yml` | 자동 배포 |
