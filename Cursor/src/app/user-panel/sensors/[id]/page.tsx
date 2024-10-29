'use client'

import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { 
  ArrowLeft,
  MapPin,
  Activity,
  Droplets,
  Thermometer,
  Waves,
  ArrowDownUp,
  Eye,
  Globe
} from 'lucide-react'
import { useApp } from "@/contexts/AppContext"
import { getSensorData } from '@/lib/boqu-api'
import { useToast } from "@/components/ui/use-toast"
import HistoricalReportDialog from '@/components/HistoricalReportDialog'
import { sensorDataCache } from '@/contexts/AppContext'

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
  lastFetched?: number
}

function formatValue(value: string, decimals: number = 2): string {
  const num = parseFloat(value)
  return isNaN(num) ? value : num.toFixed(decimals)
}

function adjustTimestamp(timestamp: string): string {
  const date = new Date(timestamp)
  date.setHours(date.getHours() - 4)
  return date.toLocaleString()
}

export default function SensorDetail({ params }: { params: { id: string } }) {
  const router = useRouter()
  const { sensors } = useApp()
  const { toast } = useToast()
  const [sensorData, setSensorData] = useState<SensorData | null>(() => {
    // Initialize from cache if available
    return sensorDataCache[params.id] || null
  })
  const [isLoading, setIsLoading] = useState(!sensorDataCache[params.id])
  const [isHistoricalReportOpen, setIsHistoricalReportOpen] = useState(false)
  
  const sensor = sensors.find(s => s.id === params.id)

  useEffect(() => {
    const fetchSensorData = async () => {
      if (!sensor?.apiId) return

      // Check cache first
      const cachedData = sensorDataCache[params.id]
      const now = Date.now()

      if (cachedData?.lastFetched && (now - cachedData.lastFetched < 30 * 60 * 1000)) {
        setSensorData(cachedData)
        setIsLoading(false)
        return
      }
      
      try {
        const data = await getSensorData(sensor.apiId)
        const newData = {
          ...data,
          lastFetched: now
        }
        // Update both state and cache
        setSensorData(newData)
        sensorDataCache[params.id] = newData
      } catch (error) {
        console.error('Error fetching sensor data:', error)
        toast({
          variant: "destructive",
          title: "Error",
          description: "Failed to fetch sensor data. Please try again later.",
        })
      } finally {
        setIsLoading(false)
      }
    }

    // Only fetch if we don't have cached data or if it's expired
    if (!sensorDataCache[params.id] || 
        (Date.now() - sensorDataCache[params.id].lastFetched! >= 30 * 60 * 1000)) {
      fetchSensorData()
    } else {
      setIsLoading(false)
    }
  }, [params.id, sensor?.apiId, toast])

  if (!sensor) {
    return <div>Sensor not found</div>
  }

  const metrics = sensorData ? [
    {
      title: "Salinity",
      value: formatValue(sensorData.Salinity),
      unit: "ppt",
      icon: Droplets
    },
    {
      title: "DO",
      value: formatValue(sensorData.DO),
      unit: "mg/L",
      icon: Activity
    },
    {
      title: "pH",
      value: formatValue(sensorData.pH),
      unit: "pH",
      icon: Activity
    },
    {
      title: "Temperature",
      value: formatValue(sensorData.Temp),
      unit: "°C",
      icon: Thermometer
    },
    {
      title: "Conductivity",
      value: formatValue(sensorData.Cond),
      unit: "mS/cm",
      icon: ArrowDownUp
    },
    {
      title: "Depth",
      value: formatValue(sensorData.Depth),
      unit: "m",
      icon: Waves
    },
    {
      title: "Turbidity",
      value: formatValue(sensorData.Turbidity),
      unit: "NTU",
      icon: Eye
    },
    {
      title: "Location",
      value: `${formatValue(sensorData.Latitude, 6)}, ${formatValue(sensorData.Longitude, 6)}`,
      unit: "",
      icon: Globe
    }
  ] : []

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button 
            variant="ghost" 
            size="icon"
            onClick={() => router.push('/user-panel')}
          >
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h2 className="text-3xl font-bold tracking-tight">{sensor.name}</h2>
            <p className="text-muted-foreground">
              <span className="inline-flex items-center gap-1">
                <MapPin className="h-4 w-4" />
                {sensor.location}
              </span>
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className={`inline-flex h-2.5 w-2.5 rounded-full ${
            sensor.status === 'online' ? 'bg-green-500' : 'bg-red-500'
          }`} />
          <span className="text-sm text-muted-foreground">
            {sensor.status === 'online' ? 'Online' : 'Offline'}
          </span>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {isLoading ? (
          <div className="col-span-full text-center py-12">
            Loading sensor data...
          </div>
        ) : metrics.map((metric) => (
          <Card key={metric.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {metric.title}
              </CardTitle>
              <metric.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {metric.value} {metric.unit && <span className="text-sm font-normal text-muted-foreground">{metric.unit}</span>}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                {sensorData?.timestamp ? adjustTimestamp(sensorData.timestamp) : ''}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="mt-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Historical Data</CardTitle>
            <Button 
              variant="outline"
              onClick={() => setIsHistoricalReportOpen(true)}
            >
              Historical Report
            </Button>
          </CardHeader>
          <CardContent>
            <div className="h-[400px] flex items-center justify-center text-muted-foreground">
              Historical data visualization coming soon...
            </div>
          </CardContent>
        </Card>
      </div>

      <HistoricalReportDialog
        isOpen={isHistoricalReportOpen}
        onClose={() => setIsHistoricalReportOpen(false)}
        sensorId={params.id}
        sensorName={sensor.name}
      />
    </div>
  )
}
