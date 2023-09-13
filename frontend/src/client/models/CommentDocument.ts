/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type CommentDocument = {
    /**
     * MongoDB document ObjectID
     */
    _id: (string | null);
    content: string;
    author: {
id: string;
collection: string;
};
    disabled: boolean;
    is_reply: boolean;
    replies: Array<{
id: string;
collection: string;
}>;
    created_at: (string | null);
    updated_at: (string | null);
};
