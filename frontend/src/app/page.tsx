'use client'
// app/page.tsx – Dashboard

import { useEffect, useState } from 'react'
import { getSummary, getExpenses, type Summary, type Expense } from '@/lib/api'
import {
  DollarSign, TrendingUp, Briefcase, User,
  Receipt, ArrowUpRight, BarChart3
} from 'lucide-react'
import Link from 'next/link'
import { clsx } from 'clsx'

function fmt(n: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}

function StatCard({
  label, value, sub, icon: Icon, color, delay = 0
}: {
  label: string; value: string; sub?: string
  icon: React.ElementType; color: string; delay?: number
}) {
  return (
    <div
      className="card p-6 flex flex-col gap-4 opacity-0 animate-fade-up"
      style={{ animationDelay: `${delay}ms`, animationFillMode: 'forwards' }}
    >
      <div className="flex items-start justify-between">
        <p className="text-sm font-medium text-slate-400">{label}</p>
        <div className={clsx('w-10 h-10 rounded-xl flex items-center justify-center', color)}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      <div>
        <p className="text-3xl font-bold text-white tracking-tight">{value}</p>
        {sub && <p className="text-sm text-slate-500 mt-1">{sub}</p>}
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [summary, setSummary] = useState<Summary | null>(null)
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getSummary(), getExpenses()])
      .then(([s, e]) => { setSummary(s); setExpenses(e) })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const recentExpenses = expenses.slice(-5).reverse()

  // Category breakdown
  const catMap: Record<string, number> = {}
  expenses.forEach(e => {
    catMap[e.category] = (catMap[e.category] ?? 0) + e.amount
  })
  const topCats = Object.entries(catMap)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
  const maxCat = topCats[0]?.[1] ?? 1

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div
        className="opacity-0 animate-fade-up"
        style={{ animationFillMode: 'forwards' }}
      >
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-slate-400 mt-1">Your tax filing overview</p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
        <StatCard
          label="Total Expenses"
          value={loading ? '—' : fmt(summary?.total_expenses ?? 0)}
          sub={`${summary?.expense_count ?? 0} bills`}
          icon={DollarSign}
          color="bg-brand-500/15 text-brand-400"
          delay={0}
        />
        <StatCard
          label="Total GST"
          value={loading ? '—' : fmt(summary?.total_gst ?? 0)}
          sub="Recoverable tax"
          icon={TrendingUp}
          color="bg-amber-500/15 text-amber-400"
          delay={60}
        />
        <StatCard
          label="Business"
          value={loading ? '—' : fmt(summary?.business_expenses ?? 0)}
          sub="Deductible"
          icon={Briefcase}
          color="bg-violet-500/15 text-violet-400"
          delay={120}
        />
        <StatCard
          label="Personal"
          value={loading ? '—' : fmt(summary?.personal_expenses ?? 0)}
          icon={User}
          color="bg-emerald-500/15 text-emerald-400"
          delay={180}
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Category breakdown */}
        <div
          className="card p-6 xl:col-span-2 opacity-0 animate-fade-up"
          style={{ animationDelay: '240ms', animationFillMode: 'forwards' }}
        >
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-brand-400" />
              <h2 className="font-semibold text-white">Spending by Category</h2>
            </div>
          </div>
          {topCats.length === 0 ? (
            <p className="text-slate-500 text-sm py-8 text-center">No expenses yet</p>
          ) : (
            <div className="space-y-4">
              {topCats.map(([cat, amt]) => (
                <div key={cat}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-slate-300 font-medium">{cat}</span>
                    <span className="text-slate-400 font-mono">{fmt(amt)}</span>
                  </div>
                  <div className="h-2 rounded-full bg-surface overflow-hidden">
                    <div
                      className="h-full rounded-full bg-brand-500 transition-all duration-700"
                      style={{ width: `${(amt / maxCat) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Bills */}
        <div
          className="card p-6 opacity-0 animate-fade-up"
          style={{ animationDelay: '300ms', animationFillMode: 'forwards' }}
        >
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <Receipt className="w-5 h-5 text-brand-400" />
              <h2 className="font-semibold text-white">Recent Bills</h2>
            </div>
            <Link href="/expenses" className="text-xs text-brand-400 hover:text-brand-300 flex items-center gap-1">
              View all <ArrowUpRight className="w-3 h-3" />
            </Link>
          </div>
          {recentExpenses.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-slate-500 text-sm">No bills uploaded yet</p>
              <Link href="/upload" className="btn-primary mt-4 inline-flex text-sm">
                Upload a bill
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {recentExpenses.map(exp => (
                <div
                  key={exp.id}
                  className="flex items-center justify-between py-2 border-b border-surface-border last:border-0"
                >
                  <div>
                    <p className="text-sm font-medium text-slate-200 truncate max-w-[140px]">
                      {exp.vendor}
                    </p>
                    <p className="text-xs text-slate-500">{exp.category}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-mono font-semibold text-white">{fmt(exp.amount)}</p>
                    <span className={clsx(
                      'text-xs',
                      exp.expense_type === 'Business' ? 'text-violet-400' : 'text-emerald-400'
                    )}>
                      {exp.expense_type}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Quick actions */}
      <div
        className="opacity-0 animate-fade-up"
        style={{ animationDelay: '360ms', animationFillMode: 'forwards' }}
      >
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { href: '/upload',   label: 'Upload New Bill',     desc: 'Drag & drop or browse',  icon: '📄' },
            { href: '/expenses', label: 'Manage Expenses',     desc: 'Edit, categorise & sort', icon: '🗂️' },
            { href: '/reports',  label: 'Generate Tax Report', desc: 'Export to Excel',         icon: '📊' },
          ].map(({ href, label, desc, icon }) => (
            <Link
              key={href}
              href={href}
              className="card p-5 flex items-start gap-4 hover:border-brand-500/50 hover:bg-brand-500/5 transition-all group"
            >
              <span className="text-2xl">{icon}</span>
              <div>
                <p className="font-semibold text-white group-hover:text-brand-300 transition-colors">{label}</p>
                <p className="text-sm text-slate-500">{desc}</p>
              </div>
              <ArrowUpRight className="w-4 h-4 text-slate-600 group-hover:text-brand-400 ml-auto mt-1 transition-colors" />
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
