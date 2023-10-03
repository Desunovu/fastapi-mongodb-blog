/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ArticleCreateOrUpdate } from '../models/ArticleCreateOrUpdate';
import type { ArticleResponse } from '../models/ArticleResponse';
import type { ArticlesResponse } from '../models/ArticlesResponse';
import type { ArticlesSortField } from '../models/ArticlesSortField';
import type { Body_change_user_role_users__user_id__role_put } from '../models/Body_change_user_role_users__user_id__role_put';
import type { Body_login_for_access_token_token_post } from '../models/Body_login_for_access_token_token_post';
import type { CommentCreate } from '../models/CommentCreate';
import type { CommentResponse } from '../models/CommentResponse';
import type { CommentsResponse } from '../models/CommentsResponse';
import type { CommentsSortField } from '../models/CommentsSortField';
import type { CommentUpdate } from '../models/CommentUpdate';
import type { RegisterRequestBody } from '../models/RegisterRequestBody';
import type { ReplyCreate } from '../models/ReplyCreate';
import type { SortDirection } from '../models/SortDirection';
import type { TokenResponseBody } from '../models/TokenResponseBody';
import type { UpdateUserPasswordRequest } from '../models/UpdateUserPasswordRequest';
import type { UpdateUserRequest } from '../models/UpdateUserRequest';
import type { UserDocument } from '../models/UserDocument';
import type { UserResponse } from '../models/UserResponse';
import type { UsersResponse } from '../models/UsersResponse';
import type { UsersSortField } from '../models/UsersSortField';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DefaultService {

    /**
     * Login For Access Token
     * Выдает токен доступа аутентифицированному пользователю
     * @param formData 
     * @returns TokenResponseBody Successful Response
     * @throws ApiError
     */
    public static loginForAccessTokenTokenPost(
formData: Body_login_for_access_token_token_post,
): CancelablePromise<TokenResponseBody> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Register User
     * Создает нового пользователя
     * @param requestBody 
     * @returns UserDocument Successful Response
     * @throws ApiError
     */
    public static registerUserRegisterPost(
requestBody: RegisterRequestBody,
): CancelablePromise<UserDocument> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/register',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * List Articles
     * Возвращает список статей.
     * @param skip 
     * @param limit 
     * @param sortBy 
     * @param sortOrder 
     * @param tag Тег для поиска статей
     * @param searchQuery Поисковый запрос для поиска статей
     * @returns ArticlesResponse Successful Response
     * @throws ApiError
     */
    public static listArticlesArticlesGet(
skip?: (number | null),
limit?: (number | null),
sortBy?: ArticlesSortField,
sortOrder?: SortDirection,
tag?: (string | null),
searchQuery?: (string | null),
): CancelablePromise<ArticlesResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/articles/',
            query: {
                'skip': skip,
                'limit': limit,
                'sort_by': sortBy,
                'sort_order': sortOrder,
                'tag': tag,
                'search_query': searchQuery,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Article
     * Создает новую статью.
     * @param requestBody 
     * @returns ArticleResponse Successful Response
     * @throws ApiError
     */
    public static createArticleArticlesPost(
requestBody: ArticleCreateOrUpdate,
): CancelablePromise<ArticleResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/articles/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Article
     * Возвращает статью по ее uuid.
     * @param articleId 
     * @returns ArticleResponse Successful Response
     * @throws ApiError
     */
    public static readArticleArticlesArticleIdGet(
articleId: string,
): CancelablePromise<ArticleResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/articles/{article_id}',
            path: {
                'article_id': articleId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Article
     * Обновляет статью по id
     * @param articleId 
     * @param requestBody 
     * @returns ArticleResponse Successful Response
     * @throws ApiError
     */
    public static updateArticleArticlesArticleIdPut(
articleId: string,
requestBody: ArticleCreateOrUpdate,
): CancelablePromise<ArticleResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/articles/{article_id}',
            path: {
                'article_id': articleId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Article
     * Удаляет статью по ее uuid
     * @param articleId 
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteArticleArticlesArticleIdDelete(
articleId: string,
): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/articles/{article_id}',
            path: {
                'article_id': articleId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * List Comments
     * Возвращает список комментариев к статье
     * @param articleId 
     * @param skip 
     * @param limit 
     * @param sortBy 
     * @param sortOrder 
     * @returns CommentsResponse Successful Response
     * @throws ApiError
     */
    public static listCommentsCommentsGet(
articleId: string,
skip?: (number | null),
limit?: (number | null),
sortBy?: CommentsSortField,
sortOrder?: SortDirection,
): CancelablePromise<CommentsResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/comments/',
            query: {
                'article_id': articleId,
                'skip': skip,
                'limit': limit,
                'sort_by': sortBy,
                'sort_order': sortOrder,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Comment
     * Создает новый комментарий к статье.
     * @param requestBody 
     * @returns CommentResponse Successful Response
     * @throws ApiError
     */
    public static createCommentCommentsPost(
requestBody: CommentCreate,
): CancelablePromise<CommentResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/comments/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Reply
     * Создает комментарий-ответ на комментарий
     * @param requestBody 
     * @returns CommentResponse Successful Response
     * @throws ApiError
     */
    public static createReplyCommentsReplyPost(
requestBody: ReplyCreate,
): CancelablePromise<CommentResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/comments/reply',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Comment
     * Обновляет комментарий по id
     * @param commentId 
     * @param requestBody 
     * @returns CommentResponse Successful Response
     * @throws ApiError
     */
    public static updateCommentCommentsCommentIdPut(
commentId: string,
requestBody: CommentUpdate,
): CancelablePromise<CommentResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/comments/{comment_id}',
            path: {
                'comment_id': commentId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Comment
     * Удаляет комментарий по id
     * @param commentId 
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteCommentCommentsCommentIdDelete(
commentId: string,
): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/comments/{comment_id}',
            path: {
                'comment_id': commentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * List Users
     * Возвращает список пользователей
     * @param skip 
     * @param limit 
     * @param sortBy 
     * @param sortOrder 
     * @returns UsersResponse Successful Response
     * @throws ApiError
     */
    public static listUsersUsersGet(
skip?: (number | null),
limit?: (number | null),
sortBy?: UsersSortField,
sortOrder?: SortDirection,
): CancelablePromise<UsersResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/',
            query: {
                'skip': skip,
                'limit': limit,
                'sort_by': sortBy,
                'sort_order': sortOrder,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Current User
     * Возвращает текущего пользователя
     * @returns UserResponse Successful Response
     * @throws ApiError
     */
    public static readCurrentUserUsersMeGet(): CancelablePromise<UserResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/me',
        });
    }

    /**
     * Get User By Id
     * Возвращает пользователя по id
     * @param userId UUID Пользователя
     * @returns UserResponse Successful Response
     * @throws ApiError
     */
    public static getUserByIdUsersUserIdGet(
userId: string,
): CancelablePromise<UserResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update User
     * Обновляет данные пользователя по id
     * @param userId UUID Пользователя
     * @param requestBody 
     * @returns UserResponse Successful Response
     * @throws ApiError
     */
    public static updateUserUsersUserIdPut(
userId: string,
requestBody: UpdateUserRequest,
): CancelablePromise<UserResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/{user_id}',
            path: {
                'user_id': userId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update User Password
     * Обновляет пароль пользователя по id
     * @param userId UUID Пользователя
     * @param requestBody 
     * @returns any Successful Response
     * @throws ApiError
     */
    public static updateUserPasswordUsersUserIdPasswordPut(
userId: string,
requestBody: UpdateUserPasswordRequest,
): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/{user_id}/password',
            path: {
                'user_id': userId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Disable User
     * Заблокировать пользователя по id [АДМИНИСТРАТОР]
     * @param userId UUID пользователя
     * @returns any Successful Response
     * @throws ApiError
     */
    public static disableUserUsersUserIdDisablePut(
userId: string,
): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/{user_id}/disable',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Change User Role
     * Изменить роль пользователя по id [АДМИНИСТРАТОР]
     * @param userId UUID пользователя
     * @param requestBody 
     * @returns any Successful Response
     * @throws ApiError
     */
    public static changeUserRoleUsersUserIdRolePut(
userId: string,
requestBody: Body_change_user_role_users__user_id__role_put,
): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/{user_id}/role',
            path: {
                'user_id': userId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
