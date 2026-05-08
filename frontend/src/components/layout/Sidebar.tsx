'use client'
// components/layout/Sidebar.tsx

import Link from 'next/link'
import { useRouter, usePathname } from 'next/navigation'
import {
  LayoutDashboard,
  Upload,
  Receipt,
  FileSpreadsheet,
  Zap,
  LogOut,
} from 'lucide-react'
import { clsx } from 'clsx'
import { useAuth } from '@/hooks/useAuth'

const NAV = [
  { href: '/expenses',   label: 'Dashboard', icon: LayoutDashboard },
  { href: '/upload',     label: 'Upload Bill', icon: Upload },
  { href: '/expenses',   label: 'Expenses',   icon: Receipt },
  { href: '/reports',    label: 'Reports',    icon: FileSpreadsheet },
]

export default function Sidebar() {
  const path = usePathname()
  const router = useRouter()
  const { user, isLoading, isAuthenticated, logout } = useAuth()

  if (!isAuthenticated) {
    return null
  }

  const handleLogout = () => {
    logout()
    router.push('/auth/login')
  }

  return (
    <aside className="w-64 shrink-0 flex flex-col bg-surface-card border-r border-surface-border h-full">
      {/* Logo */}
      <div className="px-6 py-6 border-b border-surface-border">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-brand-500 flex items-center justify-center shadow-lg shadow-brand-500/30">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="font-bold text-white leading-tight text-sm">SmartTax</p>
            <p className="text-xs text-slate-400 leading-tight">Assist</p>
          </div>
        </div>
      </div>

      {/* Nav links */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {NAV.map(({ href, label, icon: Icon }) => {
          const active = path === href
          return (
            <Link
              key={href}
              href={href}
              className={clsx(
                'flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150',
                active
                  ? 'bg-brand-500 text-white shadow-md shadow-brand-500/30'
                  : 'text-slate-400 hover:text-white hover:bg-white/5'
              )}
            >
              <Icon className="w-4.5 h-4.5 shrink-0" size={18} />
              {label}
            </Link>
          )
        })}
      </nav>

      {/* User Info & Logout */}
      <div className="px-6 py-4 border-t border-surface-border space-y-4">
        {user && (
          <div className="text-sm">
            <p className="text-slate-400 text-xs">Logged in as</p>
            <p className="text-white font-medium truncate">{user.full_name}</p>
            <p className="text-slate-500 text-xs truncate">{user.email}</p>
          </div>
        )}
        
        <button
          onClick={handleLogout}
          className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-all duration-150 text-sm font-medium"
        >
          <LogOut className="w-4 h-4" />
          Logout
        </button>

        <p className="text-xs text-slate-500">v1.0.0 · Bills never stored</p>
      </div>
    </aside>
  )
}

