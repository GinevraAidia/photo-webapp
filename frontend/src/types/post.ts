export interface Post {
  id: number
  event: number
  username_utente: string
  description: string
  image: string | null
}

export interface PostFormData {
  description: string
  image: File | null
}

export interface ReactionType {
  id: number
  name: string
  symbol: string
}

export interface PostReaction {
  id: number
  post: number
  reaction: number
  reaction_name: string
  reaction_symbol: string
  username_utente: string
}
export interface Event {
  id: number
  title: string
  description: string
  visibility: 'public' | 'private'
  users: number[]
}

export type EventFormData = Pick<
  Event,
  'title' | 'description' | 'visibility' | 'users'
>