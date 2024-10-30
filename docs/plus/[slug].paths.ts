import { readItems } from '@clairview/sdk';
import { client } from '../.vitepress/lib/clairview.js';

export default {
	async paths() {
		const articles = (
			await client.request(
				readItems('dplus_docs_articles', {
					fields: ['*'],
				}),
			)
		).map((article) => ({
			params: {
				slug: article.slug,
				title: article.title,
			},
			content: article.content,
		}));

		return articles;
	},
};
