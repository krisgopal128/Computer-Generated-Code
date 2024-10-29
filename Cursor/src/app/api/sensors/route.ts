import { NextResponse } from 'next/server'
import db from '@/lib/db'

interface Sensor {
  id: string
  equipmentId: string
  apiId: string
  name: string
  location: string
  status: 'online' | 'offline'
  item: string
}

export async function GET() {
  try {
    const sensors = db.prepare('SELECT * FROM sensors').all()
    return NextResponse.json(sensors)
  } catch (error) {
    console.error('Error fetching sensors:', error)
    return NextResponse.json(
      { error: 'Failed to fetch sensors' },
      { status: 500 }
    )
  }
}

export async function POST(request: Request) {
  try {
    const sensor = await request.json()
    
    // Validate required fields
    if (!sensor.equipmentId || !sensor.apiId || !sensor.name || !sensor.location || !sensor.status || !sensor.item) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }

    // Check for duplicate equipment ID only
    const existingEquipment = db.prepare('SELECT id FROM sensors WHERE equipmentId = ? COLLATE NOCASE').get(sensor.equipmentId)
    if (existingEquipment) {
      return NextResponse.json(
        { error: 'Equipment ID already exists' },
        { status: 409 }
      )
    }

    sensor.id = Math.random().toString(36).substr(2, 9)
    
    const stmt = db.prepare(`
      INSERT INTO sensors (id, equipmentId, apiId, name, location, status, item)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `)
    
    stmt.run(
      sensor.id,
      sensor.equipmentId.trim(),
      sensor.apiId.trim(),
      sensor.name,
      sensor.location,
      sensor.status,
      sensor.item
    )
    
    return NextResponse.json(sensor)
  } catch (error) {
    console.error('Error creating sensor:', error)
    return NextResponse.json(
      { error: 'Failed to create sensor' },
      { status: 500 }
    )
  }
}

export async function PUT(request: Request) {
  try {
    const sensor = await request.json()
    
    // Validate required fields
    if (!sensor.id || !sensor.equipmentId || !sensor.apiId || !sensor.name || !sensor.location || !sensor.status || !sensor.item) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }

    // Check for duplicate equipment ID (excluding current sensor)
    const existingEquipment = db.prepare('SELECT id FROM sensors WHERE equipmentId = ? COLLATE NOCASE AND id != ?')
      .get(sensor.equipmentId, sensor.id)
    if (existingEquipment) {
      return NextResponse.json(
        { error: 'Equipment ID already exists' },
        { status: 409 }
      )
    }
    
    const stmt = db.prepare(`
      UPDATE sensors 
      SET equipmentId = ?, apiId = ?, name = ?, location = ?, status = ?, item = ?
      WHERE id = ?
    `)
    
    const result = stmt.run(
      sensor.equipmentId.trim(),
      sensor.apiId.trim(),
      sensor.name,
      sensor.location,
      sensor.status,
      sensor.item,
      sensor.id
    )

    if (result.changes === 0) {
      return NextResponse.json(
        { error: 'Sensor not found' },
        { status: 404 }
      )
    }
    
    return NextResponse.json(sensor)
  } catch (error) {
    console.error('Error updating sensor:', error)
    return NextResponse.json(
      { error: 'Failed to update sensor' },
      { status: 500 }
    )
  }
}

export async function DELETE(request: Request) {
  try {
    const { id } = await request.json()
    
    if (!id) {
      return NextResponse.json(
        { error: 'Missing sensor ID' },
        { status: 400 }
      )
    }

    const stmt = db.prepare('DELETE FROM sensors WHERE id = ?')
    const result = stmt.run(id)

    if (result.changes === 0) {
      return NextResponse.json(
        { error: 'Sensor not found' },
        { status: 404 }
      )
    }
    
    return NextResponse.json({ id })
  } catch (error) {
    console.error('Error deleting sensor:', error)
    return NextResponse.json(
      { error: 'Failed to delete sensor' },
      { status: 500 }
    )
  }
} 