import { NavLink, Outlet } from 'react-router-dom'

export function AppShell() {
  return (
    <div className="app-shell">
      <header>
        <div className="brand">
          <span className="brand-mark">CA</span>
          <span>Company Application</span>
        </div>
        <nav aria-label="Primary">
          <NavLink to="/projects">Projects</NavLink>
        </nav>
      </header>
      <main id="main-content">
        <Outlet />
      </main>
      <footer>Production scaffold · React + FastAPI + SQLite</footer>
    </div>
  )
}
