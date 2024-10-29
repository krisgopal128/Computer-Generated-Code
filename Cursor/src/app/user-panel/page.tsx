'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Search, Battery, MapPin, ArrowRight } from 'lucide-react'
import { useApp } from "@/contexts/AppContext"
import * as api from '@/lib/api'

interface AccessibleSensor {
  id: string
  equipmentId: string
  name: string
  location: string
  status: 'online' | 'offline'
  item: string
  permissions: {
    view: boolean
    control: boolean
    configure: boolean
  }
}

const UserDashboard = () => {
  const router = useRouter()
  const { currentUser } = useApp()
  const [searchTerm, setSearchTerm] = useState('')
  const [accessibleSensors, setAccessibleSensors] = useState<AccessibleSensor[]>([])

  // Load accessible sensors based on access rules
  useEffect(() => {
    const loadAccessibleSensors = async () => {
      try {
        // Get all access rules
        const accessRules = await api.getAccessRules()
        
        // Filter rules for current user
        const userRules = accessRules.filter(rule => rule.userId === currentUser?.id)

        // Get all sensors
        const allSensors = await api.getSensors()

        // Map sensors with permissions
        const sensorsWithAccess = allSensors
          .filter(sensor => userRules.some(rule => rule.sensorId === sensor.id))
          .map(sensor => {
            const rule = userRules.find(rule => rule.sensorId === sensor.id)
            return {
              ...sensor,
              permissions: {
                view: Boolean(rule?.view),
                control: Boolean(rule?.control),
                configure: Boolean(rule?.configure),
              }
            }
          })
          // Only show sensors where user has at least view permission
          .filter(sensor => sensor.permissions.view)

        setAccessibleSensors(sensorsWithAccess)
      } catch (error) {
        console.error('Error loading accessible sensors:', error)
      }
    }

    if (currentUser) {
      loadAccessibleSensors()
    }
  }, [currentUser])

  const filteredSensors = accessibleSensors.filter(sensor =>
    sensor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    sensor.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
    sensor.item.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">My Sensors</h2>
        <div className="relative w-64">
          <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search sensors..."
            className="pl-8"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {filteredSensors.map((sensor) => (
          <Card 
            key={sensor.id}
            className="cursor-pointer hover:shadow-lg transition-shadow"
            onClick={() => router.push(`/user-panel/sensors/${sensor.id}`)}
          >
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-lg font-medium">
                {sensor.name}
              </CardTitle>
              <span className={`flex h-2.5 w-2.5 rounded-full ${
                sensor.status === 'online' ? 'bg-green-500' : 'bg-red-500'
              }`} />
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <span>{sensor.location}</span>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium">{sensor.item}</p>
                  <div className="flex gap-2 mt-1">
                    {sensor.permissions.control && (
                      <span className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded">
                        Control
                      </span>
                    )}
                    {sensor.permissions.configure && (
                      <span className="text-xs bg-purple-100 text-purple-800 px-2 py-0.5 rounded">
                        Configure
                      </span>
                    )}
                  </div>
                </div>
                <ArrowRight className="h-5 w-5 text-muted-foreground" />
              </div>
            </CardContent>
          </Card>
        ))}

        {filteredSensors.length === 0 && (
          <div className="col-span-full text-center py-12 text-muted-foreground">
            {searchTerm ? (
              <p>No sensors found matching your search.</p>
            ) : (
              <p>You don't have access to any sensors yet.</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default UserDashboard
