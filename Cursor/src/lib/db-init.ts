import db from './db'

export function initializeDatabase() {
  try {
    // Check if tables exist and have data
    const userCount = db.prepare('SELECT COUNT(*) as count FROM users').get() as { count: number }
    const sensorCount = db.prepare('SELECT COUNT(*) as count FROM sensors').get() as { count: number }
    const accessCount = db.prepare('SELECT COUNT(*) as count FROM access_rules').get() as { count: number }

    // Only initialize if all tables are empty
    if (userCount.count === 0 && sensorCount.count === 0 && accessCount.count === 0) {
      // Insert default users
      const userStmt = db.prepare(`
        INSERT INTO users (id, username, name, email, role, status, lastActive, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      `)

      // Insert admin user
      userStmt.run(
        '1',
        'admin',
        'System Admin',
        'admin@system.com',
        'admin',
        'active',
        'Just now',
        'admin123'
      )

      // Insert test user
      userStmt.run(
        '2',
        'user1',
        'John User',
        'john@example.com',
        'user',
        'active',
        'Just now',
        'user123'
      )

      // Insert test viewer
      userStmt.run(
        '3',
        'viewer1',
        'Jane Viewer',
        'jane@example.com',
        'viewer',
        'active',
        'Just now',
        'viewer123'
      )

      // Insert default sensors
      const sensorStmt = db.prepare(`
        INSERT INTO sensors (id, equipmentId, apiId, name, location, status, item)
        VALUES (?, ?, ?, ?, ?, ?, ?)
      `)

      const sensors = [
        {
          id: '1',
          equipmentId: 'TEMP001',
          apiId: 'API001',
          name: 'Temperature Sensor 1',
          location: 'Building A - Room 101',
          status: 'online',
          item: 'Temperature Monitor'
        },
        {
          id: '2',
          equipmentId: 'HUM001',
          apiId: 'API002',
          name: 'Humidity Sensor 1',
          location: 'Building B - Room 201',
          status: 'online',
          item: 'Humidity Monitor'
        },
        {
          id: '3',
          equipmentId: 'PRES001',
          apiId: 'API003',
          name: 'Pressure Sensor 1',
          location: 'Building C - Room 301',
          status: 'online',
          item: 'Pressure Monitor'
        }
      ]

      sensors.forEach(sensor => {
        sensorStmt.run(
          sensor.id,
          sensor.equipmentId,
          sensor.apiId,
          sensor.name,
          sensor.location,
          sensor.status,
          sensor.item
        )
      })

      // Insert default access rules
      const accessStmt = db.prepare(`
        INSERT INTO access_rules (id, userId, sensorId, view, control, configure)
        VALUES (?, ?, ?, ?, ?, ?)
      `)

      const accessRules = [
        {
          id: '1',
          userId: '2', // user1
          sensorId: '1', // Temperature Sensor
          view: true,
          control: true,
          configure: false
        },
        {
          id: '2',
          userId: '2', // user1
          sensorId: '2', // Humidity Sensor
          view: true,
          control: false,
          configure: false
        },
        {
          id: '3',
          userId: '3', // viewer1
          sensorId: '1', // Temperature Sensor
          view: true,
          control: false,
          configure: false
        }
      ]

      accessRules.forEach(rule => {
        accessStmt.run(
          rule.id,
          rule.userId,
          rule.sensorId,
          rule.view ? 1 : 0,
          rule.control ? 1 : 0,
          rule.configure ? 1 : 0
        )
      })
    }
  } catch (error) {
    throw error
  }
} 