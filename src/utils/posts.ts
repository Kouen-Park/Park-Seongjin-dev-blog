import { getCollection } from 'astro:content';
import type { CollectionEntry } from 'astro:content';

/**
 * 글을 최신순으로 정렬해 돌려줍니다.
 *
 * 정렬 로직을 이 함수 하나로 모아둔 이유:
 * 홈(`index.astro`)과 글 목록(`blog/index.astro`)이 각자 정렬하면
 * 한쪽만 고쳤을 때 두 화면의 순서가 달라집니다.
 *
 * 같은 날짜일 때의 처리:
 * `pubDate`에 시각이 없으면 자정으로 파싱되므로, 같은 날 올린 글끼리는
 * 날짜만으로 순서가 정해지지 않습니다. 그럴 때 파일명 역순을 tiebreaker로
 * 씁니다 — 무작위처럼 보이는 순서를 막기 위한 것일 뿐이며,
 * **의도한 순서를 원하면 `pubDate`에 시각을 넣으세요**:
 *
 *   pubDate: 'Sep 24 2026 09:00'
 *   pubDate: 'Sep 24 2026 17:30'
 */
export async function getSortedPosts(): Promise<CollectionEntry<'blog'>[]> {
	const posts = await getCollection('blog');

	return posts.sort((a, b) => {
		const diff = b.data.pubDate.valueOf() - a.data.pubDate.valueOf();
		if (diff !== 0) return diff;
		// 날짜가 같을 때: 파일명 역순으로 고정
		return b.id.localeCompare(a.id);
	});
}
