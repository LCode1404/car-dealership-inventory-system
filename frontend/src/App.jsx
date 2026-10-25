
import { useCallback, useEffect, useState } from 'react'
import './index.css'

const API_URL = 'http://127.0.0.1:8000/api'

async function apiRequest(path, { token, ...options } = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    const detail = data.detail
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg).join(', ')
      : detail || 'Request failed'
    throw new Error(message)
  }

  return data
}

function formatPrice(price) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2,
  }).format(price)
}

// Decode the role for UI display only.
// The backend must enforce every permission.
function getUserRole(token) {
  try {
    const payload = token.split('.')[1]
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/')
    const binary = atob(base64)
    const bytes = Uint8Array.from(binary, (char) => char.charCodeAt(0))
    return JSON.parse(new TextDecoder().decode(bytes)).role || 'user'
  } catch {
    return 'user'
  }
}

export default function App() {
  const [token, setToken] = useState('')
  const [authMode, setAuthMode] = useState('login')
  const [authForm, setAuthForm] = useState({
    username: '',
    email: '',
    password: '',
  })

  const [vehicles, setVehicles] = useState([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)

  const [vehicleForm, setVehicleForm] = useState({
    make: '',
    model: '',
    category: '',
    price: '',
    quantity: '',
  })

  const isAdmin = token ? getUserRole(token) === 'admin' : false

  const request = useCallback(
    (path, options = {}) => apiRequest(path, { ...options, token }),
    [token],
  )

  const loadVehicles = useCallback(async () => {
    if (!token) return

    setLoading(true)
    setError('')

    try {
      const data = await request('/vehicles')
      const term = search.trim().toLowerCase()

      setVehicles(
        term
          ? data.filter((vehicle) =>
              [vehicle.make, vehicle.model, vehicle.category].some((value) =>
                value.toLowerCase().includes(term),
              ),
            )
          : data,
      )
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [request, search, token])

  useEffect(() => {
    if (token) loadVehicles()
  }, [token, loadVehicles])

  async function handleAuth(event) {
    event.preventDefault()
    setSubmitting(true)
    setError('')
    setMessage('')

    try {
      if (authMode === 'register') {
        await apiRequest('/auth/register', {
          method: 'POST',
          body: JSON.stringify(authForm),
        })

        setAuthMode('login')
        setAuthForm((current) => ({ ...current, password: '' }))
        setMessage('Account created. Please sign in.')
      } else {
        const result = await apiRequest('/auth/login', {
          method: 'POST',
          body: JSON.stringify({
            email: authForm.email,
            password: authForm.password,
          }),
        })

        setToken(result.access_token)
        setMessage('')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  async function addVehicle(event) {
    event.preventDefault()
    setSubmitting(true)
    setError('')
    setMessage('')

    try {
      await request('/vehicles', {
        method: 'POST',
        body: JSON.stringify({
          ...vehicleForm,
          price: Number(vehicleForm.price),
          quantity: Number(vehicleForm.quantity),
        }),
      })

      setVehicleForm({
        make: '',
        model: '',
        category: '',
        price: '',
        quantity: '',
      })
      setShowAddForm(false)
      setMessage('Vehicle added successfully.')
      await loadVehicles()
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  async function purchaseVehicle(vehicle) {
    if (vehicle.quantity < 1) return

    setError('')
    setMessage('')

    try {
      await request(`/vehicles/${vehicle.id}/purchase`, {
        method: 'POST',
      })
      setMessage(`${vehicle.make} ${vehicle.model} purchased successfully.`)
      await loadVehicles()
    } catch (err) {
      setError(err.message)
    }
  }

  async function restockVehicle(vehicle) {
    const value = window.prompt(
      `Enter units to add to ${vehicle.make} ${vehicle.model}:`,
    )

    if (value === null || value.trim() === '') return

    const quantity = Number(value)

    if (!Number.isSafeInteger(quantity) || quantity <= 0) {
      setError('Enter a positive whole number.')
      return
    }

    setError('')
    setMessage('')

    try {
      await request(`/vehicles/${vehicle.id}/restock`, {
        method: 'POST',
        body: JSON.stringify({ quantity }),
      })
      setMessage('Vehicle restocked successfully.')
      await loadVehicles()
    } catch (err) {
      setError(err.message)
    }
  }

  async function deleteVehicle(vehicle) {
    const confirmed = window.confirm(
      `Are you sure you want to delete ${vehicle.make} ${vehicle.model}?`,
    )

    if (!confirmed) return

    setError('')
    setMessage('')

    try {
      await request(`/vehicles/${vehicle.id}`, {
        method: 'DELETE',
      })
      setMessage('Vehicle deleted successfully.')
      await loadVehicles()
    } catch (err) {
      setError(err.message)
    }
  }

  function logout() {
    setToken('')
    setVehicles([])
    setSearch('')
    setAuthForm({ username: '', email: '', password: '' })
    setMessage('')
    setError('')
    setShowAddForm(false)
  }

  if (!token) {
    return (
      <main className="auth-page">
        <section className="auth-card">
          <div className="brand-icon">CD</div>
          <p className="eyebrow">DEALERSHIP MANAGEMENT</p>

          <h1>
            {authMode === 'login' ? 'Welcome back' : 'Create your account'}
          </h1>

          <p className="muted">
            {authMode === 'login'
              ? 'Sign in to access vehicle inventory.'
              : 'Register to manage and explore vehicles.'}
          </p>

          {error && <div className="alert alert-error">{error}</div>}
          {message && <div className="alert alert-success">{message}</div>}

          <form className="form-stack" onSubmit={handleAuth}>
            {authMode === 'register' && (
              <label>
                Username
                <input
                  required
                  minLength={3}
                  maxLength={50}
                  value={authForm.username}
                  onChange={(event) =>
                    setAuthForm({ ...authForm, username: event.target.value })
                  }
                  placeholder="Choose a username"
                />
              </label>
            )}

            <label>
              Email address
              <input
                type="email"
                required
                value={authForm.email}
                onChange={(event) =>
                  setAuthForm({ ...authForm, email: event.target.value })
                }
                placeholder="you@example.com"
              />
            </label>

            <label>
              Password
              <input
                type="password"
                required
                minLength={authMode === 'register' ? 8 : undefined}
                value={authForm.password}
                onChange={(event) =>
                  setAuthForm({ ...authForm, password: event.target.value })
                }
                placeholder={
                  authMode === 'register'
                    ? 'At least 8 characters'
                    : 'Enter your password'
                }
              />
            </label>

            <button
              className="button button-primary full-width"
              disabled={submitting}
            >
              {submitting
                ? 'Please wait...'
                : authMode === 'login'
                  ? 'Sign in'
                  : 'Create account'}
            </button>
          </form>

          <p className="switch-auth">
            {authMode === 'login'
              ? "Don't have an account?"
              : 'Already have an account?'}{' '}
            <button
              className="text-button"
              onClick={() => {
                setAuthMode(authMode === 'login' ? 'register' : 'login')
                setError('')
                setMessage('')
              }}
            >
              {authMode === 'login' ? 'Register' : 'Sign in'}
            </button>
          </p>
        </section>
      </main>
    )
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon small">CD</div>
          <div>
            <strong>CarDesk</strong>
            <span>Inventory Management</span>
          </div>
        </div>

        <div className="header-actions">
          {isAdmin && <span className="role-pill">Administrator</span>}
          <button className="button button-outline" onClick={logout}>
            Sign out
          </button>
        </div>
      </header>

      <section className="dashboard">
        <div className="page-heading">
          <div>
            <p className="eyebrow">DEALERSHIP OVERVIEW</p>
            <h1>Vehicle inventory</h1>
            <p className="muted">
              Search, review, and manage dealership stock.
            </p>
          </div>

          <button
            className="button button-primary"
            onClick={() => setShowAddForm(!showAddForm)}
          >
            {showAddForm ? 'Cancel' : '+ Add vehicle'}
          </button>
        </div>

        {error && <div className="alert alert-error">{error}</div>}
        {message && <div className="alert alert-success">{message}</div>}

        <div className="stats-grid">
          <article className="stat-card">
            <span className="stat-label">Vehicles listed</span>
            <strong>{vehicles.length}</strong>
          </article>

          <article className="stat-card">
            <span className="stat-label">Units in stock</span>
            <strong>
              {vehicles.reduce((total, vehicle) => total + vehicle.quantity, 0)}
            </strong>
          </article>

          <article className="stat-card">
            <span className="stat-label">Available models</span>
            <strong>
              {
                new Set(
                  vehicles.map((vehicle) => `${vehicle.make} ${vehicle.model}`),
                ).size
              }
            </strong>
          </article>
        </div>

        {showAddForm && (
          <section className="panel">
            <h2>Add a vehicle</h2>

            <form className="vehicle-form" onSubmit={addVehicle}>
              <label>
                Make
                <input
                  required
                  maxLength={100}
                  value={vehicleForm.make}
                  onChange={(event) =>
                    setVehicleForm({ ...vehicleForm, make: event.target.value })
                  }
                  placeholder="Toyota"
                />
              </label>

              <label>
                Model
                <input
                  required
                  maxLength={100}
                  value={vehicleForm.model}
                  onChange={(event) =>
                    setVehicleForm({ ...vehicleForm, model: event.target.value })
                  }
                  placeholder="Camry"
                />
              </label>

              <label>
                Category
                <input
                  required
                  maxLength={50}
                  value={vehicleForm.category}
                  onChange={(event) =>
                    setVehicleForm({
                      ...vehicleForm,
                      category: event.target.value,
                    })
                  }
                  placeholder="Sedan"
                />
              </label>

              <label>
                Price (₹)
                <input
                  required
                  type="number"
                  min="0.01"
                  step="0.01"
                  value={vehicleForm.price}
                  onChange={(event) =>
                    setVehicleForm({ ...vehicleForm, price: event.target.value })
                  }
                  placeholder="1500000"
                />
              </label>

              <label>
                Quantity
                <input
                  required
                  type="number"
                  min="0"
                  step="1"
                  value={vehicleForm.quantity}
                  onChange={(event) =>
                    setVehicleForm({
                      ...vehicleForm,
                      quantity: event.target.value,
                    })
                  }
                  placeholder="5"
                />
              </label>

              <button
                className="button button-primary"
                disabled={submitting}
              >
                {submitting ? 'Saving...' : 'Save vehicle'}
              </button>
            </form>
          </section>
        )}

        <section className="panel">
          <div className="inventory-heading">
            <div>
              <h2>Inventory</h2>
              <p className="muted">Browse available vehicles.</p>
            </div>

            <form
              className="search-form"
              onSubmit={(event) => {
                event.preventDefault()
                loadVehicles()
              }}
            >
              <input
                aria-label="Search vehicles"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Search make, model, category..."
              />

              <button className="button button-primary" type="submit">
                Search
              </button>

              <button
                className="button button-outline"
                type="button"
                onClick={() => setSearch('')}
              >
                Clear
              </button>
            </form>
          </div>

          {loading ? (
            <div className="empty-state">Loading vehicles...</div>
          ) : vehicles.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">⌕</div>
              <h3>No vehicles found</h3>
              <p>Try another search or add a vehicle.</p>
            </div>
          ) : (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Vehicle</th>
                    <th>Category</th>
                    <th>Price</th>
                    <th>Stock</th>
                    <th>Actions</th>
                  </tr>
                </thead>

                <tbody>
                  {vehicles.map((vehicle) => (
                    <tr key={vehicle.id}>
                      <td>
                        <strong>
                          {vehicle.make} {vehicle.model}
                        </strong>
                        <span className="secondary-text">ID: {vehicle.id}</span>
                      </td>

                      <td>
                        <span className="category-pill">{vehicle.category}</span>
                      </td>

                      <td className="price-cell">{formatPrice(vehicle.price)}</td>

                      <td>
                        <span
                          className={`stock-pill ${
                            vehicle.quantity > 0 ? 'in-stock' : 'out-stock'
                          }`}
                        >
                          {vehicle.quantity > 0
                            ? `${vehicle.quantity} available`
                            : 'Out of stock'}
                        </span>
                      </td>

                      <td>
                        <div className="action-buttons">
                          <button
                            className="button button-small button-primary"
                            disabled={vehicle.quantity < 1}
                            onClick={() => purchaseVehicle(vehicle)}
                          >
                            Purchase
                          </button>

                          {isAdmin && (
                            <>
                              <button
                                className="button button-small button-outline"
                                onClick={() => restockVehicle(vehicle)}
                              >
                                Restock
                              </button>

                              <button
                                className="button button-small button-danger"
                                onClick={() => deleteVehicle(vehicle)}
                              >
                                Delete
                              </button>
                            </>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <footer className="page-footer">
          CarDesk Inventory System · React + FastAPI
        </footer>
      </section>
    </main>
  )
}
