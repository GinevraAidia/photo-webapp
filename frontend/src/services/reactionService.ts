import api from './api'
import type { ReactionType, PostReaction } from '@/types/post'

interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export const reactionService = {

  async getTypes(): Promise<ReactionType[]> {
    const response = await api.get<ReactionType[]>(
      '/events/typeReaction/'
    )

    return response.data
  },

  async getByPost(postId: number): Promise<PostReaction[]> {
    const response = await api.get<
      PaginatedResponse<PostReaction> | PostReaction[]
    >(
      '/events/reaction/',
      {
        params: { post: postId }
      }
    )

    return Array.isArray(response.data)
      ? response.data
      : response.data.results
  },

  async setReaction(
    postId: number,
    reactionId: number
  ): Promise<PostReaction> {
    const response = await api.post<PostReaction>(
      '/events/reaction/',
      {
        post: postId,
        reaction: reactionId
      }
    )

    return response.data
  },

  async deleteReaction(reactionId: number): Promise<void> {
    await api.delete(
      `/events/reaction/${reactionId}/`
    )
  }
}