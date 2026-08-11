import { http, HttpResponse } from 'msw'
import { describe, expect, it } from 'vitest'
import { server } from '../test/server'
import { apiRequest } from './api'

describe('apiRequest', () => {
  it('turns problem details into a typed error', async () => {
    server.use(
      http.get('/api/v1/projects', () =>
        HttpResponse.json(
          {
            type: 'https://errors.example.com/conflict',
            title: 'Conflict',
            status: 409,
            detail: 'Name already exists',
            request_id: 'req-1',
          },
          { status: 409, headers: { 'Content-Type': 'application/problem+json' } },
        ),
      ),
    )

    await expect(apiRequest('/projects')).rejects.toEqual(
      expect.objectContaining({ name: 'ApiError', status: 409, requestId: 'req-1' }),
    )
  })
})
