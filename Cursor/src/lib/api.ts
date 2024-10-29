// User API functions
export async function getUsers() {
  const response = await fetch('/api/users')
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to fetch users')
  }
  return response.json()
}

export async function createUser(userData: {
  username: string
  name: string
  email: string
  role: 'admin' | 'user' | 'viewer'
  status: 'active' | 'inactive'
  password: string
  lastActive: string
}) {
  const response = await fetch('/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to create user')
  }
  return response.json()
}

export async function updateUser(userData: {
  id: string
  username: string
  name: string
  email: string
  role: 'admin' | 'user' | 'viewer'
  status: 'active' | 'inactive'
  password: string
  lastActive: string
}) {
  const response = await fetch('/api/users', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to update user')
  }
  return response.json()
}

export async function deleteUser(id: string) {
  const response = await fetch('/api/users', {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id }),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to delete user')
  }
  return response.json()
}

// Sensor API functions
export interface SensorData {
  id?: string
  equipmentId: string
  apiId: string
  name: string
  location: string
  status: 'online' | 'offline'
  item: string
}

export async function getSensors() {
  const response = await fetch('/api/sensors')
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to fetch sensors')
  }
  return response.json()
}

export async function createSensor(sensorData: SensorData) {
  const response = await fetch('/api/sensors', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(sensorData),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to create sensor')
  }
  return response.json()
}

export async function updateSensor(sensorData: SensorData & { id: string }) {
  const response = await fetch('/api/sensors', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(sensorData),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to update sensor')
  }
  return response.json()
}

export async function deleteSensor(id: string) {
  const response = await fetch('/api/sensors', {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id }),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to delete sensor')
  }
  return response.json()
}

// Access Rules API functions
export async function getAccessRules() {
  const response = await fetch('/api/access')
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to fetch access rules')
  }
  return response.json()
}

export async function createAccessRule(ruleData: {
  userId: string
  sensorId: string
  permissions: {
    view: boolean
    control: boolean
    configure: boolean
  }
}) {
  const response = await fetch('/api/access', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(ruleData),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to create access rule')
  }
  return response.json()
}

export async function updateAccessRule(ruleData: {
  id: string
  userId: string
  sensorId: string
  permissions: {
    view: boolean
    control: boolean
    configure: boolean
  }
}) {
  const response = await fetch('/api/access', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(ruleData),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to update access rule')
  }
  return response.json()
}

export async function deleteAccessRule(id: string) {
  const response = await fetch('/api/access', {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id }),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to delete access rule')
  }
  return response.json()
} 