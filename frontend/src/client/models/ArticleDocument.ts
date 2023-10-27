/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type ArticleDocument = {
    /**
     * MongoDB document ObjectID
     */
    _id?: (string | null);
    title?: (string | null);
    preview_image_url?: (string | null);
    content?: (string | null);
    tags?: (Array<string> | null);
    created_at?: (string | null);
    updated_at?: (string | null);
    author?: ({
id: string;
collection: string;
} | null);
};
