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
  DialogFooter,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Plus, Search, Edit, Trash2, MoreVertical, Eye, EyeOff } from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu"
import { useApp } from "@/contexts/AppContext"
import { useToast } from "@/components/ui/use-toast"
import * as api from '@/lib/api'

interface User {
  id: string
  username: string
  name: string
  email: string
  role: 'admin' | 'user' | 'viewer'
  status: 'active' | 'inactive'
  lastActive: string
  password: string
}

const initialUsers: User[] = [
  { 
    id: '1', 
    username: 'johndoe',
    name: 'John Doe', 
    email: 'john@example.com', 
    role: 'admin', 
    status: 'active', 
    lastActive: '2 mins ago', 
    password: 'password123' 
  },
  { 
    id: '2', 
    username: 'janesmith',
    name: 'Jane Smith', 
    email: 'jane@example.com', 
    role: 'user', 
    status: 'active', 
    lastActive: '1 hour ago', 
    password: 'password123' 
  },
  { 
    id: '3', 
    username: 'bobwilson',
    name: 'Bob Wilson', 
    email: 'bob@example.com', 
    role: 'viewer', 
    status: 'inactive', 
    lastActive: '2 days ago', 
    password: 'password123' 
  },
]

interface UserFormData {
  username: string
  name: string
  email: string
  role: 'admin' | 'user' | 'viewer'
  password: string
}

const defaultFormData: UserFormData = {
  username: '',
  name: '',
  email: '',
  role: 'user',
  password: ''
}

const UsersPage = () => {
  const { users, setUsers } = useApp()
  const { toast } = useToast()
  const [searchTerm, setSearchTerm] = useState('')
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [editingUser, setEditingUser] = useState<User | null>(null)
  const [formData, setFormData] = useState<UserFormData>(defaultFormData)
  const [showPassword, setShowPassword] = useState<{ [key: string]: boolean }>({})

  // Load users from API on mount
  useEffect(() => {
    const loadUsers = async () => {
      try {
        const loadedUsers = await api.getUsers()
        setUsers(loadedUsers)
      } catch (error) {
        console.error('Error loading users:', error)
        toast({
          variant: "destructive",
          title: "Error",
          description: "Failed to load users. Please refresh the page.",
        })
      }
    }
    loadUsers()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      if (editingUser) {
        // Update existing user
        const updatedUser = await api.updateUser({
          ...editingUser,
          ...formData,
        })
        setUsers(users.map(user => 
          user.id === updatedUser.id ? updatedUser : user
        ))
        toast({
          title: "User Updated",
          description: `User ${formData.name} has been updated successfully.`,
        })
      } else {
        // Add new user
        const newUser = await api.createUser({
          ...formData,
          status: 'active',
          lastActive: 'Just now',
        })
        setUsers([...users, newUser])
        toast({
          title: "User Added",
          description: `User ${formData.name} has been added successfully.`,
        })
      }
      
      handleDialogClose()
    } catch (error) {
      console.error('Error saving user:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to save user data. Please try again.",
      })
    }
  }

  const handleEdit = (user: User) => {
    setEditingUser(user)
    setFormData({
      username: user.username,
      name: user.name,
      email: user.email,
      role: user.role,
      password: user.password,
    })
    setIsDialogOpen(true)
  }

  const handleDelete = async (id: string) => {
    try {
      await api.deleteUser(id)
      setUsers(users.filter(user => user.id !== id))
      toast({
        title: "User Deleted",
        description: "User has been deleted successfully.",
      })
    } catch (error) {
      console.error('Error deleting user:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to delete user. Please try again.",
      })
    }
  }

  const handleResetPassword = async (id: string) => {
    try {
      const newPassword = Math.random().toString(36).slice(-8) + 
                         Math.random().toString(36).slice(-4).toUpperCase() +
                         Math.floor(Math.random() * 10);

      const user = users.find(u => u.id === id)
      if (!user) throw new Error('User not found')

      const updatedUser = await api.updateUser({
        ...user,
        password: newPassword
      })

      setUsers(users.map(u => 
        u.id === updatedUser.id ? updatedUser : u
      ))

      toast({
        title: "Password Reset Successfully",
        description: (
          <div className="mt-2 rounded-md bg-slate-950 p-4">
            <p className="text-white mb-2">New password for {user.username}:</p>
            <code className="text-green-400 font-mono">{newPassword}</code>
          </div>
        ),
        duration: 10000,
      })

      setShowPassword(prev => ({
        ...prev,
        [id]: false
      }))
    } catch (error) {
      console.error('Error resetting password:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to reset password. Please try again.",
      })
    }
  }

  const handleToggleStatus = async (id: string) => {
    try {
      const user = users.find(u => u.id === id)
      if (!user) throw new Error('User not found')

      const updatedUser = await api.updateUser({
        ...user,
        status: user.status === 'active' ? 'inactive' : 'active'
      })

      setUsers(users.map(u => 
        u.id === updatedUser.id ? updatedUser : u
      ))

      toast({
        title: "User Status Updated",
        description: `${updatedUser.name} has been ${updatedUser.status === 'active' ? 'activated' : 'deactivated'}.`,
      })
    } catch (error) {
      console.error('Error toggling user status:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to update user status. Please try again.",
      })
    }
  }

  const handleDialogClose = () => {
    setIsDialogOpen(false)
    setEditingUser(null)
    setFormData(defaultFormData)
  }

  const togglePasswordVisibility = (userId: string) => {
    setShowPassword(prev => ({
      ...prev,
      [userId]: !prev[userId]
    }))
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold tracking-tight">User Management</h2>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Add User
            </Button>
          </DialogTrigger>
          <DialogContent>
            <form onSubmit={handleSubmit}>
              <DialogHeader>
                <DialogTitle>
                  {editingUser ? 'Edit User' : 'Add New User'}
                </DialogTitle>
              </DialogHeader>
              <div className="space-y-4 py-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Username</label>
                  <Input
                    required
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Full Name</label>
                  <Input
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Email</label>
                  <Input
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Role</label>
                  <Select
                    value={formData.role}
                    onValueChange={(value: 'admin' | 'user' | 'viewer') => 
                      setFormData({ ...formData, role: value })
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select role" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="admin">Admin</SelectItem>
                      <SelectItem value="user">User</SelectItem>
                      <SelectItem value="viewer">Viewer</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Password</label>
                  <Input
                    type="password"
                    required={!editingUser}
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    placeholder={editingUser ? "Leave blank to keep current password" : "Enter password"}
                  />
                </div>
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={handleDialogClose}>
                  Cancel
                </Button>
                <Button type="submit">
                  {editingUser ? 'Update User' : 'Add User'}
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
            placeholder="Search users..."
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
              <TableHead>Username</TableHead>
              <TableHead>Full Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Password</TableHead>
              <TableHead>Last Active</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.id}>
                <TableCell className="font-medium">{user.username}</TableCell>
                <TableCell>{user.name}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    user.role === 'admin' ? 'bg-purple-100 text-purple-800' :
                    user.role === 'user' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {user.role}
                  </span>
                </TableCell>
                <TableCell>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    user.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {user.status}
                  </span>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-sm">
                      {showPassword[user.id] ? user.password : '••••••••'}
                    </span>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => togglePasswordVisibility(user.id)}
                    >
                      {showPassword[user.id] ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </TableCell>
                <TableCell>{user.lastActive}</TableCell>
                <TableCell className="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon">
                        <MoreVertical className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem onClick={() => handleEdit(user)}>
                        Edit User
                      </DropdownMenuItem>
                      <DropdownMenuItem 
                        onClick={() => handleResetPassword(user.id)}
                        className="text-blue-600"
                      >
                        Reset Password
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => handleToggleStatus(user.id)}>
                        {user.status === 'active' ? 'Deactivate' : 'Activate'} User
                      </DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem 
                        className="text-red-600"
                        onClick={() => handleDelete(user.id)}
                      >
                        Delete User
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}

export default UsersPage
