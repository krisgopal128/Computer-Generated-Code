'use client'

import { useRouter } from 'next/navigation'
import { useApp } from "@/contexts/AppContext"
import { useEffect } from 'react'

export default function HistoricalReportsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const { currentUser } = useApp()

  useEffect(() => {
    if (!currentUser || (currentUser.role !== 'user' && currentUser.role !== 'viewer')) {
      router.push('/')
    }
  }, [currentUser, router])

  if (!currentUser || (currentUser.role !== 'user' && currentUser.role !== 'viewer')) {
    return null
  }

  return children
} 