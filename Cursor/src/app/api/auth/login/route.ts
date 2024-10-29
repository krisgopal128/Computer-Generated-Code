import { NextResponse } from 'next/server'
import db from '@/lib/db'

interface User {
  id: string
  username: string
  name: string
  email: string
  role: 'admin' | 'user' | 'viewer'
  status: 'active' | 'inactive'
  lastActive: string
  password: string
}

export async function POST(request: Request) {
  try {
    const { username, password } = await request.json()

    // First, check if user exists and get all user data
    const stmt = db.prepare(`
      SELECT * FROM users 
      WHERE username = ? AND password = ?
    `)

    const user = stmt.get(username, password) as User | undefined

    if (!user) {
      return NextResponse.json(
        { error: 'Invalid credentials' },
        { status: 401 }
      )
    }

    if (user.status !== 'active') {
      return NextResponse.json(
        { error: 'Account is inactive' },
        { status: 403 }
      )
    }

    // Update last active timestamp
    const updateStmt = db.prepare(`
      UPDATE users 
      SET lastActive = ? 
      WHERE id = ?
    `)
    updateStmt.run('Just now', user.id)

    // Remove password from response
    const { password: _, ...userWithoutPassword } = user

    return NextResponse.json(userWithoutPassword)
  } catch (error) {
    return NextResponse.json(
      { error: 'Login failed' },
      { status: 500 }
    )
  }
} 