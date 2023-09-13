/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Модель для обновления пароля
 */
export type UpdateUserPasswordRequest = {
    /**
     * Новый пароль
     */
    new_password: string;
    /**
     * Старый пароль
     */
    old_password?: (string | null);
};
