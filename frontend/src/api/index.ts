import { ApiClient } from './client'

const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
export const api = new ApiClient(baseUrl)
