export interface ProblemDetails {
  type: string
  title: string
  status: number
  detail: unknown
  instance?: string
  request_id?: string
}

export class ApiError extends Error {
  readonly status: number
  readonly requestId?: string
  readonly problem: ProblemDetails

  constructor(problem: ProblemDetails) {
    super(problem.title)
    this.name = 'ApiError'
    this.status = problem.status
    this.problem = problem
    if (problem.request_id !== undefined) this.requestId = problem.request_id
  }
}

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api/v1${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...init?.headers },
  })
  if (!response.ok) {
    const contentType = response.headers.get('Content-Type') ?? ''
    if (contentType.includes('json')) {
      throw new ApiError(await response.json() as ProblemDetails)
    }
    throw new ApiError({ type: 'about:blank', title: 'Request failed', status: response.status, detail: await response.text() })
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}
