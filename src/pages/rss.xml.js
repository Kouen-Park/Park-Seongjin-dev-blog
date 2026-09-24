import rss from '@astrojs/rss';
import { SITE_DESCRIPTION, SITE_TITLE } from '../consts';
import { getSortedPosts } from '../utils/posts';

export async function GET(context) {
	// 사이트 화면과 같은 정렬을 씁니다.
	// (정렬하지 않으면 피드가 파일명 순서로 나가 최신 글이 아래에 묻힙니다)
	const posts = await getSortedPosts();

	return rss({
		title: SITE_TITLE,
		description: SITE_DESCRIPTION,
		site: context.site,
		items: posts.map((post) => ({
			...post.data,
			link: `/blog/${post.id}/`,
		})),
	});
}
