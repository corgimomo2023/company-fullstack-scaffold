import { isRouteErrorResponse, useRouteError } from 'react-router-dom'

export function RouteErrorPage() {
  const error = useRouteError()
  const status = isRouteErrorResponse(error) ? error.status : 500
  return (
    <section className="empty" role="alert">
      <p className="eyebrow">Route error</p>
      <h1>{status === 404 ? 'Page not found' : 'The page could not be loaded'}</h1>
      <p>Return to the projects page or contact support if the problem continues.</p>
      <a href="/projects">Go to projects</a>
    </section>
  )
}
