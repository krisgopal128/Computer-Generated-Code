'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import * as api from '@/lib/api'
import { getSensorData } from '@/lib/boqu-api'

interface Sensor {
  id: string
  equipmentId: string
  apiId: string
  name: string
  location: string
  status: 'online' | 'offline'
  item: string
}

interface User {
  id: string
  username: string // Added username field
  name: string
  email: string
  role: 'admin' | 'user' | 'viewer'
  status: 'active' | 'inactive'
  lastActive: string
  password: string // Add this field
}

interface AppContextType {
  sensors: Sensor[]
  setSensors: (sensors: Sensor[]) => void
  users: User[]
  setUsers: (users: User[]) => void
  currentUser: User | null
  setCurrentUser: (user: User | null) => void
  logout: () => void // Add logout function
}

const AppContext = createContext<AppContextType | undefined>(undefined)

export const sensorDataCache: { [key: string]: any } = {}

export function AppProvider({ children }: { children: ReactNode }) {
  const [sensors, setSensors] = useState<Sensor[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [currentUser, _setCurrentUser] = useState<User | null>(() => {
    // Initialize from localStorage if available
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('currentUser')
      if (saved) {
        try {
          return JSON.parse(saved)
        } catch (error) {
          console.error('Error parsing saved user:', error)
          return null
        }
      }
    }
    return null
  })

  // Load initial data only if user is authenticated
  useEffect(() => {
    if (currentUser) {
      const loadData = async () => {
        try {
          const [usersData, sensorsData] = await Promise.all([
            api.getUsers(),
            api.getSensors()
          ])
          setUsers(usersData)
          setSensors(sensorsData)
        } catch (error) {
          console.error('Error loading data:', error)
        }
      }
      loadData()
    }
  }, [currentUser])

  const prefetchSensorData = async (sensors: Sensor[]) => {
    try {
      const fetchPromises = sensors
        .filter(sensor => sensor.apiId)
        .map(async sensor => {
          try {
            const data = await getSensorData(sensor.apiId)
            sensorDataCache[sensor.id] = {
              ...data,
              lastFetched: Date.now()
            }
          } catch (error) {
            console.error(`Failed to fetch data for sensor ${sensor.id}:`, error)
          }
        })

      await Promise.all(fetchPromises)
    } catch (error) {
      console.error('Error prefetching sensor data:', error)
    }
  }

  const handleSetCurrentUser = async (user: User | null) => {
    if (user) {
      // First set the user
      _setCurrentUser(user)
      
      // Then fetch all sensors for this user
      try {
        const userSensors = await api.getSensors()
        setSensors(userSensors)
        
        // Prefetch data for all sensors
        await prefetchSensorData(userSensors)
      } catch (error) {
        console.error('Error loading sensors:', error)
      }
    } else {
      _setCurrentUser(null)
      setSensors([])
      // Clear the cache when user logs out
      Object.keys(sensorDataCache).forEach(key => delete sensorDataCache[key])
    }
  }

  const logout = () => {
    handleSetCurrentUser(null)
    setUsers([])
    localStorage.removeItem('currentUser')
    document.cookie = 'currentUser=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT'
  }

  return (
    <AppContext.Provider value={{ 
      sensors, 
      setSensors, 
      users, 
      setUsers,
      currentUser,
      setCurrentUser: handleSetCurrentUser,
      logout 
    }}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const context = useContext(AppContext)
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider')
  }
  return context
}
