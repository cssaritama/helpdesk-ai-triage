import { describe, it, expect } from 'vitest'
import { ApiClient } from '../api/client'

describe('ApiClient', () => {
  it('normalizes base URL', () => {
    const c = new ApiClient('http://localhost:8000/')
    // @ts-expect-error private access for test purposes
    expect(c.baseUrl).toBe('http://localhost:8000')
  })
})
