'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Plus, Search, Edit, Trash2 } from 'lucide-react'
import { useToast } from "@/components/ui/use-toast"
import { useApp } from "@/contexts/AppContext"
import { getSensors, createSensor, updateSensor, deleteSensor } from '@/lib/api'

interface Sensor {
  id: string
  equipmentId: string
  apiId: string
  name: string
  location: string
  status: 'online' | 'offline'
  item: string
}

interface SensorFormData {
  equipmentId: string
  apiId: string
  name: string
  location: string
  status: 'online' | 'offline'
  item: string
}

const defaultFormData: SensorFormData = {
  equipmentId: '',
  apiId: '',
  name: '',
  location: '',
  status: 'online',
  item: '',
}

const SensorsPage = () => {
  const { toast } = useToast()
  const { sensors, setSensors } = useApp()
  const [searchTerm, setSearchTerm] = useState('')
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [editingSensor, setEditingSensor] = useState<Sensor | null>(null)
  const [formData, setFormData] = useState<SensorFormData>(defaultFormData)

  // Load sensors from API on mount
  useEffect(() => {
    const loadSensors = async () => {
      try {
        const loadedSensors = await getSensors()
        setSensors(loadedSensors)
      } catch (error) {
        console.error('Error loading sensors:', error)
        toast({
          variant: "destructive",
          title: "Error",
          description: "Failed to load sensors. Please refresh the page.",
        })
      }
    }
    loadSensors()
  }, [setSensors, toast])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      if (editingSensor) {
        // Update existing sensor
        const updatedSensor = await updateSensor({
          id: editingSensor.id,
          ...formData,
        })
        setSensors(prevSensors => prevSensors.map(sensor => 
          sensor.id === updatedSensor.id ? updatedSensor : sensor
        ))
        toast({
          title: "Sensor Updated",
          description: `Sensor ${formData.name} has been updated successfully.`,
        })
      } else {
        // Add new sensor
        const newSensor = await createSensor(formData)
        setSensors(prevSensors => [...prevSensors, newSensor])
        toast({
          title: "Sensor Added",
          description: `Sensor ${formData.name} has been added successfully.`,
        })
      }
      
      handleDialogClose()
    } catch (error) {
      console.error('Error saving sensor:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to save sensor data. Please try again.",
      })
    }
  }

  const handleDelete = async (id: string) => {
    try {
      await deleteSensor(id)
      setSensors(prevSensors => prevSensors.filter(sensor => sensor.id !== id))
      toast({
        title: "Sensor Deleted",
        description: "Sensor has been deleted successfully.",
      })
    } catch (error) {
      console.error('Error deleting sensor:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to delete sensor. Please try again.",
      })
    }
  }

  const handleDialogClose = () => {
    setIsDialogOpen(false)
    setEditingSensor(null)
    setFormData(defaultFormData)
  }

  const handleEdit = (sensor: Sensor) => {
    setEditingSensor(sensor)
    setFormData({
      equipmentId: sensor.equipmentId,
      apiId: sensor.apiId,
      name: sensor.name,
      location: sensor.location,
      status: sensor.status,
      item: sensor.item,
    })
    setIsDialogOpen(true)
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold tracking-tight">Sensor Management</h2>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Add Sensor
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>
                {editingSensor ? 'Edit Sensor' : 'Add New Sensor'}
              </DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Equipment ID</label>
                <Input
                  required
                  value={formData.equipmentId}
                  onChange={(e) => setFormData({ ...formData, equipmentId: e.target.value })}
                  placeholder="Enter equipment ID"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">API ID</label>
                <Input
                  required
                  value={formData.apiId}
                  onChange={(e) => setFormData({ ...formData, apiId: e.target.value })}
                  placeholder="Enter API ID"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Name</label>
                <Input
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Enter sensor name"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Initial Location</label>
                <Input
                  required
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  placeholder="Enter initial location"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Item</label>
                <Input
                  required
                  value={formData.item}
                  onChange={(e) => setFormData({ ...formData, item: e.target.value })}
                  placeholder="Enter item description"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Status</label>
                <Select
                  value={formData.status}
                  onValueChange={(value: 'online' | 'offline') => 
                    setFormData({ ...formData, status: value })
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="online">Online</SelectItem>
                    <SelectItem value="offline">Offline</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={handleDialogClose}>
                  Cancel
                </Button>
                <Button type="submit">
                  {editingSensor ? 'Update Sensor' : 'Add Sensor'}
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="flex items-center space-x-2">
        <div className="relative flex-1">
          <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search sensors..."
            className="pl-8"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Equipment ID</TableHead>
              <TableHead>API ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Initial Location</TableHead>
              <TableHead>Item</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sensors.map((sensor) => (
              <TableRow key={sensor.id}>
                <TableCell>{sensor.equipmentId}</TableCell>
                <TableCell>{sensor.apiId}</TableCell>
                <TableCell className="font-medium">{sensor.name}</TableCell>
                <TableCell>{sensor.location}</TableCell>
                <TableCell>{sensor.item}</TableCell>
                <TableCell>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    sensor.status === 'online' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {sensor.status}
                  </span>
                </TableCell>
                <TableCell className="text-right">
                  <Button variant="ghost" size="icon" onClick={() => handleEdit(sensor)}>
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon" onClick={() => handleDelete(sensor.id)}>
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}

export default SensorsPage
