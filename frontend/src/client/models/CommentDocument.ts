/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type CommentDocument = {
  /**
   * MongoDB document ObjectID
   */
  _id: string | null
  content: string
  author: {
    _id?: string
    id: string
    collection: string
  }
  disabled: boolean
  is_reply: boolean
  replies: Array<{
    _id?: string
    author?: { _id?: string; id?: string; username?: string }
    content?: string
    id: string
    collection: string
  }>
  created_at: string | null
  updated_at: string | null
}
