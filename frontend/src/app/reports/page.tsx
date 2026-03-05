'use client'
// app/reports/page.tsx

import { useState, useEffect } from 'react'
import { getExpenses, getSummary, downloadExcel, type Expense, type Summary } from '@/lib/api'
import {
  FileSpreadsheet, Download, RefreshCw, CheckCircle2,
  TrendingUp, Briefcase, User, DollarSign, Receipt
} from 'lucide-react'
import { clsx } from 'clsx'

function fmt(n: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}

export default function ReportsPage() {
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [summary, setSummary] = useState<Summary | null>(null)
  const [loading, setLoading] = useState(true)
  const [downloading, setDownloading] = useState(false)
  const [downloaded, setDownloaded] = useState(false)

  useEffect(() => {
    Promise.all([getExpenses(), getSummary()])
      .then(([e, s]) => { setExpenses(e); setSummary(s) })
      .finally(() => setLoading(false))
  }, [])

  const handleDownload = async () => {
    setDownloading(true)
    downloadExcel()
    // Give browser a moment to trigger download, then show success state
    setTimeout(() => {
      setDownloading(false)
      setDownloaded(true)
      setTimeout(() => setDownloaded(false), 4000)
    }, 1200)
  }

  // Monthly breakdown
  const monthMap: Record<string, { amount: number; gst: number; count: number }> = {}
  expenses.forEach(e => {
    const key = e.date?.slice(0, 7) ?? 'Unknown'
    if (!monthMap[key]) monthMap[key] = { amount: 0, gst: 0, count: 0 }
    monthMap[key].amount += e.amount
    monthMap[key].gst += e.gst
    monthMap[key].count++
  })
  const months = Object.entries(monthMap).sort((a, b) => b[0].localeCompare(a[0]))

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      {/* Header */}
      <div className="opacity-0 animate-fade-up" style={{ animationFillMode: 'forwards' }}>
        <h1 className="text-2xl font-bold text-white">Tax Reports</h1>
        <p className="text-slate-400 mt-1">Generate and download your expense report for tax filing</p>
      </div>

      {/* Report card */}
      <div
        className="opacity-0 animate-fade-up card p-8 space-y-6"
        style={{ animationDelay: '60ms', animationFillMode: 'forwards' }}
      >
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center">
              <FileSpreadsheet className="w-7 h-7 text-emerald-400" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">SmartTax_Report.xlsx</h2>
              <p className="text-sm text-slate-400 mt-0.5">
                {summary?.expense_count ?? 0} bills · Expenses + Summary sheets
              </p>
            </div>
          </div>
          <button
            onClick={handleDownload}
            disabled={downloading || loading || !summary?.expense_count}
            className={clsx(
              'flex items-center gap-2 font-semibold px-6 py-3 rounded-xl transition-all duration-200 active:scale-95',
              downloaded
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                : 'btn-primary',
              (downloading || loading) && 'opacity-70 cursor-not-allowed'
            )}
          >
            {downloading ? (
              <><RefreshCw className="w-4 h-4 animate-spin" /> Generating…</>
            ) : downloaded ? (
              <><CheckCircle2 className="w-4 h-4" /> Downloaded!</>
            ) : (
              <><Download className="w-4 h-4" /> Download Excel</>
            )}
          </button>
        </div>

        <div className="h-px bg-surface-border" />

        {/* Summary stats in report card */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Total Expenses', value: fmt(summary?.total_expenses ?? 0), icon: DollarSign, color: 'text-brand-400' },
            { label: 'Total GST',      value: fmt(summary?.total_gst ?? 0),      icon: TrendingUp, color: 'text-amber-400' },
            { label: 'Business',       value: fmt(summary?.business_expenses ?? 0), icon: Briefcase, color: 'text-violet-400' },
            { label: 'Personal',       value: fmt(summary?.personal_expenses ?? 0), icon: User,     color: 'text-emerald-400' },
          ].map(({ label, value, icon: Icon, color }) => (
            <div key={label} className="bg-surface rounded-xl p-4 border border-surface-border">
              <div className="flex items-center gap-2 mb-2">
                <Icon className={clsx('w-4 h-4', color)} />
                <span className="text-xs text-slate-500 font-medium">{label}</span>
              </div>
              <p className={clsx('text-xl font-bold font-mono', loading ? 'shimmer rounded h-7' : 'text-white')}>
                {loading ? '' : value}
              </p>
            </div>
          ))}
        </div>

        {/* Report contents breakdown */}
        <div>
          <h3 className="text-sm font-semibold text-slate-400 mb-3">Report Columns</h3>
          <div className="flex flex-wrap gap-2">
            {['Bill Name', 'Vendor', 'Category', 'Expense Type', 'Amount ($)', 'GST ($)', 'Date'].map(col => (
              <span
                key={col}
                className="px-3 py-1 rounded-lg bg-brand-500/10 border border-brand-500/20 text-brand-300 text-xs font-medium font-mono"
              >
                {col}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Monthly breakdown */}
      {months.length > 0 && (
        <div
          className="opacity-0 animate-fade-up card p-6 space-y-4"
          style={{ animationDelay: '180ms', animationFillMode: 'forwards' }}
        >
          <div className="flex items-center gap-2">
            <Receipt className="w-5 h-5 text-brand-400" />
            <h2 className="font-semibold text-white">Monthly Summary</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-surface-border">
                  <th className="text-left py-2.5 text-xs font-semibold text-slate-400 uppercase tracking-wide">Month</th>
                  <th className="text-center py-2.5 text-xs font-semibold text-slate-400 uppercase tracking-wide">Bills</th>
                  <th className="text-right py-2.5 text-xs font-semibold text-slate-400 uppercase tracking-wide">Amount</th>
                  <th className="text-right py-2.5 text-xs font-semibold text-slate-400 uppercase tracking-wide">GST</th>
                </tr>
              </thead>
              <tbody>
                {months.map(([month, data]) => (
                  <tr key={month} className="border-b border-surface-border last:border-0 hover:bg-white/[0.02]">
                    <td className="py-3 text-slate-300 font-medium">{month}</td>
                    <td className="py-3 text-center text-slate-400">{data.count}</td>
                    <td className="py-3 text-right font-mono text-white">{fmt(data.amount)}</td>
                    <td className="py-3 text-right font-mono text-amber-400">{fmt(data.gst)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* No data notice */}
      {!loading && expenses.length === 0 && (
        <div
          className="opacity-0 animate-fade-up card p-12 text-center"
          style={{ animationDelay: '120ms', animationFillMode: 'forwards' }}
        >
          <FileSpreadsheet className="w-12 h-12 text-slate-600 mx-auto mb-4" />
          <p className="text-slate-400 font-medium">No expenses to report yet</p>
          <p className="text-sm text-slate-500 mt-1">Upload some bills first, then generate your report.</p>
        </div>
      )}
    </div>
  )
}
