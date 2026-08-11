import { Navigate, createBrowserRouter } from 'react-router-dom'
import { AppShell } from '../App'
import { RouteErrorPage } from './RouteErrorPage'

export const router = createBrowserRouter([
  {
    path: '/',
    Component: AppShell,
    ErrorBoundary: RouteErrorPage,
    children: [
      { index: true, element: <Navigate to="/projects" replace /> },
      {
        path: 'projects',
        lazy: async () => {
          const module = await import('../features/projects/ProjectsPage')
          return { Component: module.ProjectsPage }
        },
      },
      { path: '*', element: <Navigate to="/projects" replace /> },
    ],
  },
])
