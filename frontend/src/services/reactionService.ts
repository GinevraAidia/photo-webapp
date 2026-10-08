import api from './api';
import type { Reaction,Emoji } from '@/types/post';
interface PaginatedResponse<T> {
        count: number
        next: string | null
        previous: string | null
        results: T[]
        }
export const reactionService={
    async getByPost(postId: number): Promise<Reaction[]> {
        const response = await api.get<PaginatedResponse<Reaction>>(
        '/events/reaction/',
        {
            params: { post: postId }
        }
        )

        return response.data.results
    },
    async setReaction(postId:number,emoji:Emoji):Promise<Reaction>{
        const response = await api.post(`events/reaction/`,{
            post:postId,
            emoji:emoji
        })
        return response.data
    },
    async deleteReaction(reactionId:number):Promise<void>{
        await api.delete(`events/reaction/${reactionId}/`)
    }

}