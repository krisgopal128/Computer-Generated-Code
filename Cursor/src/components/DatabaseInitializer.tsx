'use client'

import { useEffect } from 'react'

async function initDB() {
  try {
    const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'
    await fetch(`${baseUrl}/api/init`)
  } catch (error) {
    console.error('Failed to initialize database:', error)
  }
}

export default function DatabaseInitializer() {
  useEffect(() => {
    initDB()
  }, [])
  return null
} 