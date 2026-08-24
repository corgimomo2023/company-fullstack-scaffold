import { NavLink, Outlet } from 'react-router-dom'

export function AppShell() {
  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">
        Skip to main content
      </a>
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">CA</span>
          <span>Company Application</span>
        </div>
        <nav aria-label="Primary">
          <NavLink to="/projects">Projects</NavLink>
        </nav>
      </header>
      <main id="main-content" tabIndex={-1}>
        <Outlet />
      </main>
      <footer>Production scaffold · React + FastAPI + SQLite</footer>
    </div>
  )
}
