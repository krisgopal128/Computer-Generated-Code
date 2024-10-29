'use client'

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { 
  Activity, 
  Users, 
  Radio, 
  AlertTriangle 
} from "lucide-react"
import { useApp } from "@/contexts/AppContext"

const DashboardPage = () => {
  const { sensors, users } = useApp()

  const stats = [
    {
      title: "Total Sensors",
      value: sensors.length.toString(),
      icon: Radio,
      description: "Active sensors in the system"
    },
    {
      title: "Active Users",
      value: users.length.toString(),
      icon: Users,
      description: "Total registered users"
    },
    {
      title: "System Status",
      value: "98.5%",
      icon: Activity,
      description: "Overall system uptime"
    },
    {
      title: "Active Alerts",
      value: sensors.filter(s => s.status === 'offline').length.toString(),
      icon: AlertTriangle,
      description: "Offline sensors"
    }
  ]

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold tracking-tight">Dashboard Overview</h2>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.title}
              </CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">
                {stat.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

export default DashboardPage
