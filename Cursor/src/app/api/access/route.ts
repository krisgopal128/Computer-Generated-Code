import { NextResponse } from 'next/server'
import db from '@/lib/db'

interface AccessRule {
  id: string
  userId: string
  userName: string
  sensorId: string
  sensorName: string
  view: boolean
  control: boolean
  configure: boolean
}

export async function GET() {
  try {
    // Join with users and sensors tables to get names
    const rules = db.prepare(`
      SELECT 
        ar.id,
        ar.userId,
        u.name as userName,
        ar.sensorId,
        s.name as sensorName,
        ar.view,
        ar.control,
        ar.configure
      FROM access_rules ar
      JOIN users u ON ar.userId = u.id
      JOIN sensors s ON ar.sensorId = s.id
    `).all() as AccessRule[]

    return NextResponse.json(rules)
  } catch (error) {
    console.error('Error fetching access rules:', error)
    return NextResponse.json(
      { error: 'Failed to fetch access rules' },
      { status: 500 }
    )
  }
}

export async function POST(request: Request) {
  try {
    const rule = await request.json()

    // Validate required fields
    if (!rule.userId || !rule.sensorId) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }

    // Check if user and sensor exist
    const user = db.prepare('SELECT name FROM users WHERE id = ?').get(rule.userId)
    const sensor = db.prepare('SELECT name FROM sensors WHERE id = ?').get(rule.sensorId)

    if (!user || !sensor) {
      return NextResponse.json(
        { error: 'User or sensor not found' },
        { status: 404 }
      )
    }

    // Check for duplicate rule
    const existing = db.prepare('SELECT id FROM access_rules WHERE userId = ? AND sensorId = ?')
      .get(rule.userId, rule.sensorId)

    if (existing) {
      return NextResponse.json(
        { error: 'Access rule already exists' },
        { status: 409 }
      )
    }

    rule.id = Math.random().toString(36).substr(2, 9)
    
    const stmt = db.prepare(`
      INSERT INTO access_rules (id, userId, sensorId, view, control, configure)
      VALUES (?, ?, ?, ?, ?, ?)
    `)
    
    stmt.run(
      rule.id,
      rule.userId,
      rule.sensorId,
      rule.permissions.view ? 1 : 0,
      rule.permissions.control ? 1 : 0,
      rule.permissions.configure ? 1 : 0
    )

    // Return complete rule with names
    const newRule = db.prepare(`
      SELECT 
        ar.id,
        ar.userId,
        u.name as userName,
        ar.sensorId,
        s.name as sensorName,
        ar.view,
        ar.control,
        ar.configure
      FROM access_rules ar
      JOIN users u ON ar.userId = u.id
      JOIN sensors s ON ar.sensorId = s.id
      WHERE ar.id = ?
    `).get(rule.id) as AccessRule

    return NextResponse.json(newRule)
  } catch (error) {
    console.error('Error creating access rule:', error)
    return NextResponse.json(
      { error: 'Failed to create access rule' },
      { status: 500 }
    )
  }
}

export async function PUT(request: Request) {
  try {
    const rule = await request.json()
    
    if (!rule.id) {
      return NextResponse.json(
        { error: 'Missing rule ID' },
        { status: 400 }
      )
    }

    const stmt = db.prepare(`
      UPDATE access_rules 
      SET view = ?, control = ?, configure = ?
      WHERE id = ?
    `)
    
    const result = stmt.run(
      rule.permissions.view ? 1 : 0,
      rule.permissions.control ? 1 : 0,
      rule.permissions.configure ? 1 : 0,
      rule.id
    )

    if (result.changes === 0) {
      return NextResponse.json(
        { error: 'Access rule not found' },
        { status: 404 }
      )
    }

    // Return updated rule with names
    const updatedRule = db.prepare(`
      SELECT 
        ar.id,
        ar.userId,
        u.name as userName,
        ar.sensorId,
        s.name as sensorName,
        ar.view,
        ar.control,
        ar.configure
      FROM access_rules ar
      JOIN users u ON ar.userId = u.id
      JOIN sensors s ON ar.sensorId = s.id
      WHERE ar.id = ?
    `).get(rule.id) as AccessRule
    
    return NextResponse.json(updatedRule)
  } catch (error) {
    console.error('Error updating access rule:', error)
    return NextResponse.json(
      { error: 'Failed to update access rule' },
      { status: 500 }
    )
  }
}

export async function DELETE(request: Request) {
  try {
    const { id } = await request.json()
    
    if (!id) {
      return NextResponse.json(
        { error: 'Missing rule ID' },
        { status: 400 }
      )
    }

    const stmt = db.prepare('DELETE FROM access_rules WHERE id = ?')
    const result = stmt.run(id)

    if (result.changes === 0) {
      return NextResponse.json(
        { error: 'Access rule not found' },
        { status: 404 }
      )
    }
    
    return NextResponse.json({ id })
  } catch (error) {
    console.error('Error deleting access rule:', error)
    return NextResponse.json(
      { error: 'Failed to delete access rule' },
      { status: 500 }
    )
  }
} 