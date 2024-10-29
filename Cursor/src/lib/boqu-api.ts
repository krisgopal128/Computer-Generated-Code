interface BoquToken {
  access_token: string
  expires_in: number
}

interface SensorData {
  Latitude: string
  Longitude: string
  Salinity: string
  Temp: string
  Cond: string
  DO: string
  pH: string
  Depth: string
  Turbidity: string
  timestamp: string
}

const BOQU_API = {
  baseUrl: 'https://vip.boqucloud.com/api',
  credentials: {
    grant_type: 'client_credentials',
    appKey: 'ed1c989efe294501a8ccadd00097c786',
    appSecret: 'bf5d16de48ed477081ea58e517078d25',
    account: 'Ecocoast'
  }
}

export async function getBoquToken(): Promise<string> {
  const response = await fetch(`${BOQU_API.baseUrl}/token/get`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams(BOQU_API.credentials),
  })

  if (!response.ok) {
    throw new Error('Failed to get Boqu token')
  }

  const data = await response.json()
  return data.data.access_token
}

export async function getSensorData(apiId: string): Promise<SensorData> {
  const token = await getBoquToken()
  
  // Open monitor portal first
  await fetch(`${BOQU_API.baseUrl}/eg/monitor/open`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({ equipmentId: apiId }),
  })

  // Get sensor values
  const response = await fetch(`${BOQU_API.baseUrl}/eg/signal/value`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({ equipmentId: apiId }),
  })

  if (!response.ok) {
    throw new Error('Failed to get sensor data')
  }

  const data = await response.json()
  
  // Map the signal IDs to their respective measurements
  const signalMap = {
    '2057461': 'Salinity',
    '2057456': 'Temp',
    '2057492': 'Latitude',
    '2057455': 'Cond',
    '2057459': 'DO',
    '2057457': 'pH',
    '2057491': 'Longitude',
    '2057454': 'Depth',
    '2057453': 'Turbidity'
  }

  const formattedData: any = {}
  let timestamp = ''

  Object.entries(data.data).forEach(([signalId, info]: [string, any]) => {
    if (signalMap[signalId]) {
      formattedData[signalMap[signalId]] = info.value
      timestamp = info.time // Use any timestamp, they should all be the same
    }
  })

  return {
    ...formattedData,
    timestamp
  }
} 