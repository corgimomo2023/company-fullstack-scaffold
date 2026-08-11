import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'

export const server = setupServer(
  http.get('/api/v1/projects', () =>
    HttpResponse.json({ items: [], total: 0, limit: 50, offset: 0 }),
  ),
)
