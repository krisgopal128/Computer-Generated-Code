import { NextResponse } from 'next/server'
import { initializeDatabase } from '@/lib/db-init'

export async function GET() {
  try {
    console.log('Initializing database...')
    initializeDatabase()
    console.log('Database initialized successfully')
    return NextResponse.json({ message: 'Database initialized successfully' })
  } catch (error) {
    console.error('Error initializing database:', error)
    return NextResponse.json(
      { error: 'Failed to initialize database', details: error instanceof Error ? error.message : String(error) },
      { status: 500 }
    )
  }
} 