 import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    username: ''
  }),
  actions: {
    setUser(username: string) {
      this.username=username
    },
    clearUser() {
      this.username=' ';
    }
  }
}); 