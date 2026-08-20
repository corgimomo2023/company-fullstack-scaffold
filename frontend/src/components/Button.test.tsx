import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { Button } from './Button'

describe('Button', () => {
  it('exposes a typed visual variant', () => {
    render(<Button variant="secondary">Cancel</Button>)

    expect(screen.getByRole('button', { name: 'Cancel' })).toHaveClass(
      'button',
      'button-secondary',
    )
  })

  it('keeps the action name stable while announcing pending progress', () => {
    render(
      <Button pending pendingLabel="Creating project">
        Create project
      </Button>,
    )

    const button = screen.getByRole('button', { name: 'Create project' })
    expect(button).toBeDisabled()
    expect(button).toHaveAttribute('aria-busy', 'true')
    expect(screen.getByRole('status')).toHaveTextContent('Creating project')
  })

  it('does not let caller props override the managed pending state', () => {
    render(
      <Button pending aria-busy={false} disabled={false}>
        Create project
      </Button>,
    )

    const button = screen.getByRole('button', { name: 'Create project' })
    expect(button).toBeDisabled()
    expect(button).toHaveAttribute('aria-busy', 'true')
  })
})
