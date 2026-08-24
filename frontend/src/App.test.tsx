import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it } from 'vitest'
import { AppShell } from './App'

describe('AppShell', () => {
  it('provides a functional skip link and themed header hook', () => {
    render(
      <MemoryRouter>
        <AppShell />
      </MemoryRouter>,
    )

    expect(screen.getByRole('link', { name: 'Skip to main content' })).toHaveAttribute(
      'href',
      '#main-content',
    )
    expect(screen.getByRole('banner')).toHaveClass('topbar')
    expect(screen.getByRole('main')).toHaveAttribute('tabindex', '-1')
  })
})
