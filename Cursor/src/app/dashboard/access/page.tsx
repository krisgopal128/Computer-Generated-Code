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
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Search, Shield } from 'lucide-react'
import { Checkbox } from "@/components/ui/checkbox"
import { useToast } from "@/components/ui/use-toast"
import { useApp } from '@/contexts/AppContext'
import * as api from '@/lib/api'

interface AccessRule {
  id: string
  userId: string
  userName: string
  sensorId: string
  sensorName: string
  permissions: {
    view: boolean
    control: boolean
    configure: boolean
  }
}

const AccessControlPage = () => {
  const { toast } = useToast()
  const { users, sensors } = useApp()
  const [accessRules, setAccessRules] = useState<AccessRule[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedUser, setSelectedUser] = useState<string>('')
  const [selectedSensor, setSelectedSensor] = useState<string>('')

  // Load access rules from API
  useEffect(() => {
    const loadAccessRules = async () => {
      try {
        const rules = await api.getAccessRules()
        setAccessRules(rules.map(rule => ({
          id: rule.id,
          userId: rule.userId,
          userName: rule.userName,
          sensorId: rule.sensorId,
          sensorName: rule.sensorName,
          permissions: {
            view: Boolean(rule.view),
            control: Boolean(rule.control),
            configure: Boolean(rule.configure)
          }
        })))
      } catch (error) {
        console.error('Error loading access rules:', error)
        toast({
          variant: "destructive",
          title: "Error",
          description: "Failed to load access rules. Please refresh the page.",
        })
      }
    }
    loadAccessRules()
  }, [users, sensors, toast])

  // Calculate statistics
  const statistics = {
    totalRules: accessRules.length,
    usersWithAccess: new Set(accessRules.map(rule => rule.userId)).size,
    sensorsManaged: new Set(accessRules.map(rule => rule.sensorId)).size,
    pendingRequests: 0 // This could be implemented later if needed
  }

  const handlePermissionChange = async (ruleId: string, permission: keyof AccessRule['permissions']) => {
    try {
      const rule = accessRules.find(r => r.id === ruleId)
      if (!rule) return

      const updatedRule = await api.updateAccessRule({
        id: rule.id,
        userId: rule.userId,
        sensorId: rule.sensorId,
        permissions: {
          ...rule.permissions,
          [permission]: !rule.permissions[permission],
        },
      })

      const transformedRule = {
        ...updatedRule,
        permissions: {
          view: Boolean(updatedRule.view),
          control: Boolean(updatedRule.control),
          configure: Boolean(updatedRule.configure)
        }
      }

      setAccessRules(rules => rules.map(r => 
        r.id === transformedRule.id ? transformedRule : r
      ))

      toast({
        title: "Permission Updated",
        description: "Access permission has been updated successfully.",
      })
    } catch (error) {
      console.error('Error updating permission:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to update permission. Please try again.",
      })
    }
  }

  const handleAssignAccess = async () => {
    try {
      if (!selectedUser || !selectedSensor) {
        toast({
          variant: "destructive",
          title: "Error",
          description: "Please select both a user and a sensor.",
        })
        return
      }

      const user = users.find(u => u.id === selectedUser)
      const sensor = sensors.find(s => s.id === selectedSensor)

      if (!user || !sensor) {
        toast({
          variant: "destructive",
          title: "Error",
          description: "Selected user or sensor not found.",
        })
        return
      }

      const newRule = await api.createAccessRule({
        userId: user.id,
        sensorId: sensor.id,
        permissions: {
          view: true,
          control: false,
          configure: false,
        },
      })

      const transformedRule = {
        ...newRule,
        permissions: {
          view: Boolean(newRule.view),
          control: Boolean(newRule.control),
          configure: Boolean(newRule.configure)
        }
      }

      setAccessRules([...accessRules, transformedRule])

      toast({
        title: "Access Assigned",
        description: `Access granted to ${user.name} for ${sensor.name}`,
      })

      setSelectedUser('')
      setSelectedSensor('')
    } catch (error) {
      console.error('Error assigning access:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to assign access. Please try again.",
      })
    }
  }

  const filteredRules = accessRules.filter(rule =>
    rule.userName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    rule.sensorName.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleDeleteRule = async (ruleId: string) => {
    try {
      await api.deleteAccessRule(ruleId)
      setAccessRules(rules => rules.filter(rule => rule.id !== ruleId))
      
      toast({
        title: "Access Rule Removed",
        description: "The access rule has been removed successfully.",
      })
    } catch (error) {
      console.error('Error deleting access rule:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to remove access rule. Please try again.",
      })
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Access Control</h2>
          <p className="text-muted-foreground">Manage sensor and user permissions</p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Quick Access Assignment</CardTitle>
            <CardDescription>Quickly assign access permissions to users</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Select User</label>
              <Select value={selectedUser} onValueChange={setSelectedUser}>
                <SelectTrigger>
                  <SelectValue placeholder="Select a user" />
                </SelectTrigger>
                <SelectContent>
                  {users
                    .filter(user => user.status === 'active' && user.role !== 'admin')
                    .map(user => (
                      <SelectItem key={user.id} value={user.id}>
                        {user.name}
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Select Sensor</label>
              <Select value={selectedSensor} onValueChange={setSelectedSensor}>
                <SelectTrigger>
                  <SelectValue placeholder="Select a sensor" />
                </SelectTrigger>
                <SelectContent>
                  {sensors.map(sensor => (
                    <SelectItem key={sensor.id} value={sensor.id}>
                      {sensor.name} ({sensor.location})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <Button 
              className="w-full" 
              onClick={handleAssignAccess}
              disabled={!selectedUser || !selectedSensor}
            >
              <Shield className="mr-2 h-4 w-4" />
              Assign Access
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Access Statistics</CardTitle>
            <CardDescription>Overview of current access assignments</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <p className="text-2xl font-bold">{statistics.totalRules}</p>
                <p className="text-sm text-muted-foreground">Total Access Rules</p>
              </div>
              <div className="space-y-2">
                <p className="text-2xl font-bold">{statistics.usersWithAccess}</p>
                <p className="text-sm text-muted-foreground">Users with Access</p>
              </div>
              <div className="space-y-2">
                <p className="text-2xl font-bold">{statistics.sensorsManaged}</p>
                <p className="text-sm text-muted-foreground">Sensors Managed</p>
              </div>
              <div className="space-y-2">
                <p className="text-2xl font-bold">{statistics.pendingRequests}</p>
                <p className="text-sm text-muted-foreground">Pending Requests</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="space-y-4">
        <div className="flex items-center space-x-2">
          <div className="relative flex-1">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search access rules..."
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
                <TableHead>User</TableHead>
                <TableHead>Sensor</TableHead>
                <TableHead>View</TableHead>
                <TableHead>Control</TableHead>
                <TableHead>Configure</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredRules.map((rule) => (
                <TableRow key={rule.id}>
                  <TableCell className="font-medium">{rule.userName}</TableCell>
                  <TableCell>{rule.sensorName}</TableCell>
                  <TableCell>
                    <Checkbox
                      checked={rule.permissions.view}
                      onCheckedChange={() => handlePermissionChange(rule.id, 'view')}
                    />
                  </TableCell>
                  <TableCell>
                    <Checkbox
                      checked={rule.permissions.control}
                      onCheckedChange={() => handlePermissionChange(rule.id, 'control')}
                    />
                  </TableCell>
                  <TableCell>
                    <Checkbox
                      checked={rule.permissions.configure}
                      onCheckedChange={() => handlePermissionChange(rule.id, 'configure')}
                    />
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDeleteRule(rule.id)}
                      className="text-red-600 hover:text-red-700"
                    >
                      Remove
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  )
}

export default AccessControlPage
