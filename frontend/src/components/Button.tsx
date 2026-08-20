import type { ButtonHTMLAttributes, ReactNode } from 'react'

export type ButtonVariant =
  | 'primary'
  | 'secondary'
  | 'accent'
  | 'destructive'
  | 'ghost'

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  pending?: boolean
  pendingLabel?: ReactNode
}

export function Button({
  children,
  className = '',
  disabled,
  pending = false,
  pendingLabel = 'Working',
  variant = 'primary',
  ...props
}: ButtonProps) {
  return (
    <>
      <button
        {...props}
        className={`button button-${variant} ${className}`.trim()}
        disabled={disabled || pending}
        aria-busy={pending || undefined}
      >
        <span className={pending ? 'button-label button-label-pending' : 'button-label'}>
          {children}
        </span>
        {pending ? (
          <span aria-hidden="true" className="button-pending-label">
            {pendingLabel}
          </span>
        ) : null}
      </button>
      {pending ? (
        <span aria-atomic="true" className="visually-hidden" role="status">
          {pendingLabel}
        </span>
      ) : null}
    </>
  )
}
