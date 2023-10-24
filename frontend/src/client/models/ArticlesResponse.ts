/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ArticleDocumentResponse } from './ArticleDocumentResponse';

/**
 * Модель ответа с списком статей
 */
export type ArticlesResponse = {
    articles: Array<ArticleDocumentResponse>;
    total: number;
};
