/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Модель для создания или обновления статьи. Должно быть хотя бы одно поле не None
 */
export type ArticleCreateOrUpdate = {
    title?: (string | null);
    preview_image_url?: (string | null);
    content?: (string | null);
    tags?: (Array<string> | null);
};
