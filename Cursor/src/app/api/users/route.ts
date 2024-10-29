import { NextResponse } from 'next/server'
import db from '@/lib/db'

export async function GET() {
  const users = db.prepare('SELECT * FROM users').all()
  return NextResponse.json(users)
}

export async function POST(request: Request) {
  const user = await request.json()
  user.id = Math.random().toString(36).substr(2, 9)
  
  const stmt = db.prepare(`
    INSERT INTO users (id, username, name, email, role, status, lastActive, password)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `)
  
  stmt.run(
    user.id,
    user.username,
    user.name,
    user.email,
    user.role,
    user.status,
    user.lastActive,
    user.password
  )
  
  return NextResponse.json(user)
}

export async function PUT(request: Request) {
  const user = await request.json()
  
  const stmt = db.prepare(`
    UPDATE users 
    SET username = ?, name = ?, email = ?, role = ?, status = ?, lastActive = ?, password = ?
    WHERE id = ?
  `)
  
  stmt.run(
    user.username,
    user.name,
    user.email,
    user.role,
    user.status,
    user.lastActive,
    user.password,
    user.id
  )
  
  return NextResponse.json(user)
}

export async function DELETE(request: Request) {
  const { id } = await request.json()
  
  const stmt = db.prepare('DELETE FROM users WHERE id = ?')
  stmt.run(id)
  
  return NextResponse.json({ id })
} 