import api from './api'
import type { Post, PostFormData } from '@/types/post'

function buildFormData(
  data: PostFormData,
  eventId?: number
): FormData {
  const form = new FormData()

  form.append('description', data.description)

  if (eventId !== undefined) {
    form.append('event', String(eventId))
  }

  if (data.image) {
    form.append('image', data.image)
  }

  return form
}

export const postService = {
  async getByEvent(eventId: number): Promise<Post[]> {
    const response = await api.get('/events/post/', {
      params: { event: eventId }
    })

    return response.data.results ?? response.data
  },

  async create(
    eventId: number,
    data: PostFormData
  ): Promise<Post> {
    const response = await api.post(
      '/events/post/',
      buildFormData(data, eventId)
    )

    return response.data
  },

  async update(
    postId: number,
    data: PostFormData
  ): Promise<Post> {
    const response = await api.patch(
      `/events/post/${postId}/`,
      buildFormData(data)
    )

    return response.data
  },

  async delete(postId: number): Promise<void> {
    await api.delete(`/events/post/${postId}/`)
  }
}