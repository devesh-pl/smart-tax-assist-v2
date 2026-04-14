// lib/api.ts
// Typed API client for the SmartTax Assist backend

const BASE =
  process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface Expense {
  id: string
  bill_name: string
  vendor: string
  category: string
  expense_type: 'Personal' | 'Business'
  amount: number
  gst: number
  date: string | null
}

export interface Summary {
  total_expenses: number
  total_gst: number
  business_expenses: number
  personal_expenses: number
  expense_count: number
}

export interface UploadResult extends Expense {
  raw_text: string
  message: string
}

export interface ExpenseUpdate {
  category?: string
  expense_type?: string
  vendor?: string
  amount?: number
  gst?: number
  date?: string
  bill_name?: string
}

// ── Bills ─────────────────────────────────────────────────────────────────────
export async function uploadBill(file: File): Promise<UploadResult> {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${BASE}/upload-bill`, { method: 'POST', body: form })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Upload failed' }))
    throw new Error(err.detail ?? 'Upload failed')
  }
  return res.json()
}

// ── Expenses ──────────────────────────────────────────────────────────────────
export async function getExpenses(filters?: {
  category?: string
  expense_type?: string
  month?: string
}): Promise<Expense[]> {
  const params = new URLSearchParams()
  if (filters?.category)     params.set('category', filters.category)
  if (filters?.expense_type) params.set('expense_type', filters.expense_type)
  if (filters?.month)        params.set('month', filters.month)
  const res = await fetch(`${BASE}/expenses?${params}`)
  if (!res.ok) throw new Error('Failed to fetch expenses')
  return res.json()
}

export async function getSummary(): Promise<Summary> {
  const res = await fetch(`${BASE}/expenses/summary`)
  if (!res.ok) throw new Error('Failed to fetch summary')
  return res.json()
}

export async function updateExpense(id: string, data: ExpenseUpdate): Promise<Expense> {
  const res = await fetch(`${BASE}/expenses/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error('Failed to update expense')
  return res.json()
}

export async function deleteExpense(id: string): Promise<void> {
  const res = await fetch(`${BASE}/expenses/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Failed to delete expense')
}

// ── Categories ────────────────────────────────────────────────────────────────
export async function getCategories(): Promise<string[]> {
  const res = await fetch(`${BASE}/categories`)
  if (!res.ok) throw new Error('Failed to fetch categories')
  const data = await res.json()
  return data.categories
}

export async function addCategory(name: string): Promise<string[]> {
  const res = await fetch(`${BASE}/categories`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail ?? 'Failed to add category')
  }
  const data = await res.json()
  return data.categories
}

export async function renameCategory(oldName: string, newName: string): Promise<string[]> {
  const res = await fetch(`${BASE}/categories/${encodeURIComponent(oldName)}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ new_name: newName }),
  })
  if (!res.ok) throw new Error('Failed to rename category')
  const data = await res.json()
  return data.categories
}

export async function deleteCategory(name: string): Promise<string[]> {
  const res = await fetch(`${BASE}/categories/${encodeURIComponent(name)}`, {
    method: 'DELETE',
  })
  if (!res.ok) throw new Error('Failed to delete category')
  const data = await res.json()
  return data.categories
}

// ── Export ────────────────────────────────────────────────────────────────────
export function downloadExcel(): void {
  // Open in same tab so browser triggers native download
  window.location.href = `${BASE}/export-excel`
}
