# parkseongjin.me

Gavin Park의 개발 블로그. [parkseongjin.me](https://parkseongjin.me)

## 스택

- [Astro](https://astro.build) — 정적 사이트 생성기
- GitHub Pages — 호스팅 (커스텀 도메인 `parkseongjin.me`)
- GitHub Actions — `main`에 push하면 자동 빌드·배포
- [Pretendard](https://github.com/orioncactus/pretendard) — 본문 폰트 (한글 대응)

## 새 글 쓰기

`src/content/blog/` 에 마크다운(`.md`) 또는 MDX(`.mdx`) 파일을 추가합니다.
**파일명이 URL이 됩니다** — `next16-hydration.md` → `/blog/next16-hydration/`.
파일명은 영문 소문자와 하이픈을 쓰세요 (한글 파일명은 URL이 인코딩되어 지저분해집니다).

```markdown
---
title: 'Next 16에서 페이지가 하이드레이션되지 않던 이유'
description: '컴포넌트 버그를 3시간 찾았는데 원인은 dev 서버의 cross-origin 차단이었다.'
pubDate: 'Sep 24 2026'
heroImage: '../../assets/posts/next16-hydration.png'   # 선택
updatedDate: 'Sep 26 2026'                             # 선택
---

본문...
```

| 필드 | 필수 | 설명 |
|---|---|---|
| `title` | ✅ | 글 제목 |
| `description` | ✅ | 목록·SEO·OG 태그에 쓰이는 한 줄 요약. **2줄까지만 표시**되니 120자 안쪽 |
| `pubDate` | ✅ | 발행일. `'Sep 24 2026'` 또는 `'2026-09-24'` |
| `heroImage` | | 대표 이미지. 목록 썸네일 + 글 상단 + OG 이미지로 함께 쓰임 |
| `updatedDate` | | 수정일. 넣으면 글 상단에 표시 |

커밋하고 push하면 몇 분 안에 사이트에 반영됩니다.

## 이미지 넣는 방법

이미지는 **`src/assets/` 아래에 두고 상대경로로 참조**합니다. 이러면 Astro가 빌드할 때
WebP로 변환하고 크기를 최적화하며, 경로가 틀리면 **빌드가 실패해서** 깨진 이미지가
배포되는 일을 막아줍니다.

`public/` 에 두면 최적화가 되지 않고 오타도 잡아주지 않으니, 파비콘 같은 것만 두세요.

### 1. 대표 이미지 (heroImage)

목록의 썸네일과 글 상단 이미지, 그리고 SNS 공유 카드에 함께 쓰입니다.

```bash
# 글마다 하나씩, 파일명은 글 파일명과 맞추면 찾기 쉽습니다
src/assets/posts/next16-hydration.png
```

```markdown
---
title: '...'
heroImage: '../../assets/posts/next16-hydration.png'
---
```

경로는 **글 파일 기준 상대경로**입니다. `src/content/blog/` 에서 `src/assets/` 로
올라가야 하므로 `../../assets/` 로 시작합니다.

권장 규격:
- **가로세로 비율 3:2 또는 2:1** — 썸네일(104×70)과 상단 이미지(1020×510) 양쪽에서 잘 보입니다
- **가로 1200px 이상** — 상단 이미지가 1020px로 렌더되므로 그보다 크게
- PNG(스크린샷·다이어그램) 또는 JPG(사진). Astro가 WebP로 변환하니 원본 포맷은 편한 대로

`heroImage`는 **선택 항목**입니다. 없으면 목록에서 썸네일 칸 없이 제목이
전체 폭을 쓰도록 되어 있어서 레이아웃이 깨지지 않습니다.

### 2. 본문 속 이미지

마크다운 문법을 그대로 쓰면 됩니다.

```markdown
![스크린샷 설명](../../assets/posts/next16-devtools.png)
```

대괄호 안의 설명(alt 텍스트)은 **비워두지 마세요** — 스크린리더 사용자와
이미지가 로드되지 않은 경우에 이 텍스트만 남습니다. 순수 장식용 이미지라면
`![](...)` 로 비워두는 것이 오히려 맞습니다.

MDX(`.mdx`)에서 크기를 직접 지정하려면 `<Image>` 컴포넌트를 쓸 수 있습니다:

```mdx
import { Image } from 'astro:assets';
import shot from '../../assets/posts/shot.png';

<Image src={shot} alt="설정 화면" width={720} />
```

### 3. 정리 규칙

```
src/assets/
├── posts/                    ← 글에 쓰는 이미지 (권장)
│   ├── next16-hydration.png
│   └── rag-citations.png
└── blog-placeholder-*.jpg    ← 템플릿 기본 이미지 (이미지 없는 글의 OG 폴백)
```

## 디자인

터미널 감각의 UI 크롬 + 읽기 편한 한글 본문 조합입니다.

- **UI 크롬은 모노스페이스** — 프롬프트(`parkseongjin.me:~$`), 날짜, 파일명, 섹션 라벨(`$ ls -t posts/`)
- **제목·본문은 Pretendard(sans)** — 긴 한국어 글의 가독성 확보
- **이미지는 '파일 프리뷰'로 처리** — 점선 테두리로 감싸 터미널 맥락에 녹아들게

### 색을 바꾸거나 추가할 때

모든 색은 `src/styles/global.css` 상단의 CSS 커스텀 프로퍼티로 정의되어 있습니다.
라이트(`:root`)와 다크(`html[data-theme='dark']`) 두 세트를 **반드시 함께** 수정하세요.

```css
:root {
	--accent: #0f7b4f;        /* 라이트 */
}
html[data-theme='dark'] {
	--accent: #4ade80;        /* 다크 */
}
```

컴포넌트에서 색상값을 직접 쓰면 테마 전환 시 깨집니다. 항상 `var(--토큰명)`을 쓰세요.

### 다크모드 동작

1. 첫 방문 — OS 설정(`prefers-color-scheme`)을 따릅니다
2. 헤더 우측 버튼으로 전환 — 선택이 `localStorage`에 저장되어 다음 방문에도 유지됩니다
3. 직접 고른 적이 없다면 OS 설정을 바꿀 때 실시간으로 따라갑니다

테마는 `BaseHead.astro`의 **인라인 스크립트가 `<head>`에서 동기 실행**하여 적용합니다.
이걸 지연시키거나 번들로 옮기면 다크모드 사용자가 페이지를 열 때 흰 화면이
한 프레임 번쩍입니다(FOUC). `is:inline`을 유지하세요.

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
| `src/content.config.ts` | 글 frontmatter 스키마 |
| `src/assets/posts/` | 글에 쓰는 이미지 |
| `src/pages/` | 페이지 (홈, 글 목록, 글 상세, 소개, RSS) |
| `src/layouts/BlogPost.astro` | 글·소개 페이지 레이아웃 |
| `src/components/PostRow.astro` | 글 목록의 한 줄 (썸네일 + 제목 + 요약) |
| `src/components/ThemeToggle.astro` | 다크모드 토글 |
| `src/styles/global.css` | 디자인 토큰 + 전역 스타일 |
| `src/consts.ts` | 사이트 제목·설명 |
| `public/` | 정적 파일 (favicon, CNAME) |
| `.github/workflows/deploy.yml` | 자동 배포 |

## 배포

`main`에 push하면 GitHub Actions가 빌드해서 Pages로 배포합니다.

설정상 주의할 점 두 가지:

- **Pages Source는 "GitHub Actions"** 여야 합니다. "Deploy from a branch"로 두면
  레거시 Jekyll 빌드가 돌아 실패합니다.
- **workflow의 `node-version: 22`를 낮추지 마세요.** `withastro/action`의 기본값은
  Node 20인데 astro 7은 Node 22.12 이상을 요구해서 빌드가 즉시 실패합니다.
