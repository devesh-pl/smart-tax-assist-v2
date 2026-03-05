'use client'
// app/upload/page.tsx – Bill upload with drag-and-drop

import { useState, useCallback, useRef, DragEvent, ChangeEvent } from 'react'
import { uploadBill, type UploadResult } from '@/lib/api'
import {
  Upload, CheckCircle2, AlertCircle, FileText,
  X, Loader2, Eye, RefreshCw
} from 'lucide-react'
import { clsx } from 'clsx'
import Link from 'next/link'

type Status = 'idle' | 'dragging' | 'uploading' | 'success' | 'error'

function fmt(n: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}

export default function UploadPage() {
  const [status, setStatus] = useState<Status>('idle')
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [result, setResult] = useState<UploadResult | null>(null)
  const [error, setError] = useState<string>('')
  const [showRaw, setShowRaw] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const reset = () => {
    setStatus('idle')
    setFile(null)
    setPreview(null)
    setResult(null)
    setError('')
    setShowRaw(false)
  }

  const handleFile = useCallback((f: File) => {
    if (!['image/jpeg', 'image/png', 'application/pdf'].includes(f.type)) {
      setError('Only JPG, PNG, or PDF files are supported.')
      setStatus('error')
      return
    }
    setFile(f)
    setError('')
    // Image preview
    if (f.type.startsWith('image/')) {
      const reader = new FileReader()
      reader.onload = e => setPreview(e.target?.result as string)
      reader.readAsDataURL(f)
    } else {
      setPreview(null)
    }
    setStatus('idle')
  }, [])

  const handleDrop = useCallback((e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setStatus('idle')
    const dropped = e.dataTransfer.files[0]
    if (dropped) handleFile(dropped)
  }, [handleFile])

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (f) handleFile(f)
  }

  const handleSubmit = async () => {
    if (!file) return
    setStatus('uploading')
    try {
      const data = await uploadBill(file)
      setResult(data)
      setStatus('success')
    } catch (err: any) {
      setError(err.message ?? 'Upload failed')
      setStatus('error')
    }
  }

  return (
    <div className="p-8 max-w-3xl mx-auto space-y-8">
      {/* Header */}
      <div className="opacity-0 animate-fade-up" style={{ animationFillMode: 'forwards' }}>
        <h1 className="text-2xl font-bold text-white">Upload Bill</h1>
        <p className="text-slate-400 mt-1">
          Bills are processed in memory only — never stored permanently.
        </p>
      </div>

      {status !== 'success' ? (
        <>
          {/* Drop Zone */}
          <div
            className={clsx(
              'opacity-0 animate-fade-up card border-2 border-dashed rounded-2xl transition-all duration-200 cursor-pointer',
              status === 'dragging' ? 'border-brand-500 bg-brand-500/8' : 'border-surface-border hover:border-brand-500/50 hover:bg-white/[0.02]'
            )}
            style={{ animationDelay: '60ms', animationFillMode: 'forwards' }}
            onDragOver={e => { e.preventDefault(); setStatus('dragging') }}
            onDragLeave={() => setStatus('idle')}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
          >
            <input
              ref={inputRef}
              type="file"
              accept=".jpg,.jpeg,.png,.pdf"
              className="hidden"
              onChange={handleChange}
            />

            {file ? (
              <div className="p-8 flex items-center gap-5">
                {preview ? (
                  <img
                    src={preview}
                    alt="bill preview"
                    className="w-24 h-24 object-cover rounded-xl border border-surface-border"
                  />
                ) : (
                  <div className="w-24 h-24 rounded-xl bg-surface border border-surface-border flex items-center justify-center">
                    <FileText className="w-10 h-10 text-slate-500" />
                  </div>
                )}
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-white truncate">{file.name}</p>
                  <p className="text-sm text-slate-400 mt-1">
                    {(file.size / 1024).toFixed(1)} KB · {file.type}
                  </p>
                </div>
                <button
                  className="p-2 rounded-lg hover:bg-red-500/10 text-slate-500 hover:text-red-400 transition-colors"
                  onClick={e => { e.stopPropagation(); reset() }}
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="p-12 flex flex-col items-center text-center gap-4">
                <div className="w-16 h-16 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center">
                  <Upload className="w-8 h-8 text-brand-400" />
                </div>
                <div>
                  <p className="font-semibold text-white">Drop your bill here</p>
                  <p className="text-sm text-slate-500 mt-1">or click to browse · JPG, PNG, PDF up to 10 MB</p>
                </div>
              </div>
            )}
          </div>

          {/* Error */}
          {status === 'error' && (
            <div className="flex items-center gap-3 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400">
              <AlertCircle className="w-5 h-5 shrink-0" />
              <p className="text-sm">{error}</p>
            </div>
          )}

          {/* Actions */}
          {file && (
            <div
              className="opacity-0 animate-fade-up flex gap-3"
              style={{ animationDelay: '120ms', animationFillMode: 'forwards' }}
            >
              <button onClick={handleSubmit} className="btn-primary flex items-center gap-2" disabled={status === 'uploading'}>
                {status === 'uploading' ? (
                  <><Loader2 className="w-4 h-4 animate-spin" /> Extracting data…</>
                ) : (
                  <><Upload className="w-4 h-4" /> Process Bill</>
                )}
              </button>
              <button onClick={reset} className="btn-ghost">Clear</button>
            </div>
          )}
        </>
      ) : result ? (
        /* Success – extracted data card */
        <div
          className="opacity-0 animate-fade-up space-y-6"
          style={{ animationFillMode: 'forwards' }}
        >
          {/* Success banner */}
          <div className="flex items-center gap-3 p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
            <CheckCircle2 className="w-5 h-5 shrink-0" />
            <p className="text-sm font-medium">Bill processed and added to your expenses.</p>
          </div>

          {/* Extracted fields */}
          <div className="card p-6 space-y-5">
            <h2 className="font-semibold text-white flex items-center gap-2">
              <FileText className="w-4 h-4 text-brand-400" />
              Extracted Information
            </h2>
            <div className="grid grid-cols-2 gap-4">
              {[
                { label: 'File',     value: result.bill_name },
                { label: 'Vendor',   value: result.vendor },
                { label: 'Date',     value: result.date ?? '—' },
                { label: 'Category', value: result.category },
                { label: 'Amount',   value: fmt(result.amount) },
                { label: 'GST',      value: fmt(result.gst) },
              ].map(({ label, value }) => (
                <div key={label} className="bg-surface rounded-xl p-4 border border-surface-border">
                  <p className="text-xs text-slate-500 font-medium uppercase tracking-wide">{label}</p>
                  <p className="text-white font-semibold mt-1 truncate">{value}</p>
                </div>
              ))}
            </div>

            {/* Raw OCR text toggle */}
            {result.raw_text && (
              <div>
                <button
                  className="flex items-center gap-2 text-sm text-brand-400 hover:text-brand-300 transition-colors"
                  onClick={() => setShowRaw(!showRaw)}
                >
                  <Eye className="w-4 h-4" />
                  {showRaw ? 'Hide' : 'Show'} raw OCR text
                </button>
                {showRaw && (
                  <pre className="mt-3 p-4 rounded-xl bg-surface border border-surface-border text-xs text-slate-400 font-mono whitespace-pre-wrap max-h-48 overflow-y-auto">
                    {result.raw_text}
                  </pre>
                )}
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <button onClick={reset} className="btn-primary flex items-center gap-2">
              <RefreshCw className="w-4 h-4" /> Upload Another
            </button>
            <Link href="/expenses" className="btn-ghost">
              View All Expenses →
            </Link>
          </div>
        </div>
      ) : null}
    </div>
  )
}
