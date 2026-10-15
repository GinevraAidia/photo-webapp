import type { UserFormData } from "@/types/post"
import api from "./api"

export const userService={
    async update( data: UserFormData): Promise<UserFormData> {
    const response = await api.patch<UserFormData>(
    '/events/users/me/',
    data
  )
  return response.data
    }
}