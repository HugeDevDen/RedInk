import { defineStore } from 'pinia'

export interface AuthState {
  token: string | null
  username: string | null
  isAuthenticated: boolean
}

const TOKEN_KEY = 'auth-token'
const USERNAME_KEY = 'auth-username'

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => {
    const savedToken = localStorage.getItem(TOKEN_KEY)
    const savedUsername = localStorage.getItem(USERNAME_KEY)
    return {
      token: savedToken,
      username: savedUsername,
      isAuthenticated: !!savedToken
    }
  },

  getters: {
    isLoggedIn: (state): boolean => state.isAuthenticated
  },

  actions: {
    async login(username: string, password: string) {
      const { login } = await import('../api')
      const result = await login(username, password)

      if (result.success && result.token) {
        this.token = result.token
        this.username = result.username || username
        this.isAuthenticated = true

        localStorage.setItem(TOKEN_KEY, result.token)
        localStorage.setItem(USERNAME_KEY, result.username || username)

        return true
      }

      return false
    },

    async verify() {
      const { verifyToken } = await import('../api')
      const result = await verifyToken()

      if (result.valid) {
        this.username = result.username || this.username
        this.isAuthenticated = true
        return true
      }

      this.logout()
      return false
    },

    logout() {
      this.token = null
      this.username = null
      this.isAuthenticated = false

      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(USERNAME_KEY)
    }
  }
})
