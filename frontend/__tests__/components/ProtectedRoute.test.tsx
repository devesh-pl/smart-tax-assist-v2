/**
 * __tests__/components/ProtectedRoute.test.tsx - Tests for ProtectedRoute component
 */
import { render, screen } from '@testing-library/react'
import ProtectedRoute from '@/components/ProtectedRoute'

// Mock useAuth hook
jest.mock('@/hooks/useAuth', () => ({
  __esModule: true,
  useAuth: () => ({
    user: { id: '1', email: 'test@example.com' },
    loading: false,
    isAuthenticated: true,
  }),
}))

describe('ProtectedRoute Component', () => {
  it('renders protected content when authenticated', () => {
    render(<ProtectedRoute><div>Protected Content</div></ProtectedRoute>)
    expect(screen.getByText('Protected Content')).toBeInTheDocument()
  })
})
