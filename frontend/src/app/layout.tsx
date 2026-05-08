// app/layout.tsx
import type { Metadata } from 'next'
import './globals.css'
import { AuthProvider } from '@/context/AuthContext'

export const metadata: Metadata = {
  title: 'SmartTax Assist',
  description: 'Intelligent bill management and tax reporting',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="flex h-screen overflow-hidden bg-surface text-slate-200">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
