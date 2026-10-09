import api from './api'
import type { Event, EventFormData } from '@/types/post'
interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export const eventService = {

  // GET: recupera gli eventi
  async getAll(): Promise<Event[]> {
    const response = await api.get<
      PaginatedResponse<Event> | Event[]
    >('/events/event/')

    return Array.isArray(response.data)
      ? response.data
      : response.data.results
  },

  // GET: recupera un singolo evento
  async getById(id: number): Promise<Event> {
    const response = await api.get<Event>(
      `/events/event/${id}/`
    )

    return response.data
  },

  // DELETE: elimina un evento
  async delete(id: number): Promise<void> {
    await api.delete(`/events/event/${id}/`)
  },

  async update(id: number, data: EventFormData): Promise<Event> {
  const response = await api.patch<Event>(
    `/events/event/${id}/`,
    data
  )
  return response.data
    },
    async create(data: EventFormData): Promise<Event> {
        const response = await api.post<Event>('/events/event/', data)
        return response.data
    }
}