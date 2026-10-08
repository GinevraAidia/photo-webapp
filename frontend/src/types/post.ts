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

/* export type Emoji =
  | 'like'
  | 'dislike'
  | 'heart'
  | 'laugh'

export interface Reaction {
  id: number
  post: number
  user: number
  username_utente: string
  emoji: Emoji
} */
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