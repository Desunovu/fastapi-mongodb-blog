/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CommentDocument } from './CommentDocument';
import type { UserDocument } from './UserDocument';

/**
 * Модель для ответа с fetch_links=True
 */
export type CommentDocumentResponse = {
    /**
     * MongoDB document ObjectID
     */
    _id?: (string | null);
    content: string;
    author: UserDocument;
    disabled?: boolean;
    is_reply?: boolean;
    replies: Array<CommentDocument>;
    created_at?: (string | null);
    updated_at?: (string | null);
};
