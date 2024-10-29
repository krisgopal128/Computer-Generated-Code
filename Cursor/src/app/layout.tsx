import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Toaster } from "@/components/ui/toaster"
import { AppProvider } from '@/contexts/AppContext'
import DatabaseInitializer from '@/components/DatabaseInitializer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Water Quality Monitoring',
  description: 'Real-time water quality monitoring and sensor management system',
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon.ico',
    apple: '/apple-touch-icon.png',
    other: {
      rel: 'apple-touch-icon-precomposed',
      url: '/apple-touch-icon.png',
    },
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
      </head>
      <body className={inter.className}>
        <AppProvider>
          <DatabaseInitializer />
          {children}
        </AppProvider>
        <Toaster />
      </body>
    </html>
  )
}
