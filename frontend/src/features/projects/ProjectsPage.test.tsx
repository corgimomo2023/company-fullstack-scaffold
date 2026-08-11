import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { http, HttpResponse } from 'msw'
import { describe, expect, it } from 'vitest'
import { server } from '../../test/server'
import { ProjectsPage } from './ProjectsPage'

function renderPage() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return render(
    <QueryClientProvider client={client}>
      <ProjectsPage />
    </QueryClientProvider>,
  )
}

describe('ProjectsPage', () => {
  it('renders projects from the API', async () => {
    server.use(
      http.get('/api/v1/projects', () =>
        HttpResponse.json({
          items: [
            {
              id: 1,
              name: 'Company Portal',
              description: null,
              status: 'active',
              version: 1,
              created_at: '2026-01-01T00:00:00Z',
              updated_at: '2026-01-01T00:00:00Z',
            },
          ],
          total: 1,
          limit: 50,
          offset: 0,
        }),
      ),
    )
    renderPage()
    expect(screen.getByText('Loading projects...')).toBeInTheDocument()
    expect(await screen.findByText('Company Portal')).toBeInTheDocument()
  })

  it('validates project name before submission', async () => {
    renderPage()
    await screen.findByText('No projects yet')
    await userEvent.click(screen.getByRole('button', { name: 'Create project' }))
    expect(await screen.findByText('Name must be at least 2 characters')).toBeInTheDocument()
  })
})
