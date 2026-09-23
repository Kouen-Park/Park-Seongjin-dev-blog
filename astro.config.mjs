// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	site: 'https://parkseongjin.me',
	integrations: [mdx(), sitemap()],
	// 폰트는 BaseHead.astro에서 Pretendard(한글 대응)를 로드합니다.
	// Astro의 fonts API는 쓰지 않습니다 — Pretendard dynamic-subset이
	// 글자 단위 woff2를 필요한 만큼만 내려받는 방식이라 더 효율적입니다.
});
