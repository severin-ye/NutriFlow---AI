export interface User {
    email: string
    password: string
    name: string
    age: number
    weight: number
    height: number
}

export interface AuthState {
    isAuthenticated: boolean
    user: User | null
}
