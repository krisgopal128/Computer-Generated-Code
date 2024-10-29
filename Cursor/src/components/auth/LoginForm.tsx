'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Checkbox } from '@/components/ui/checkbox'
import { useToast } from '@/components/ui/use-toast'
import { Loader2 } from 'lucide-react'
import { useApp } from "@/contexts/AppContext"

export default function LoginForm() {
  const router = useRouter()
  const { toast } = useToast()
  const { setCurrentUser } = useApp()
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    rememberMe: false
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Login failed')
      }

      // Set user data in context and localStorage
      setCurrentUser(data)
      if (formData.rememberMe) {
        localStorage.setItem('currentUser', JSON.stringify(data))
      }

      // Set cookie for authentication
      document.cookie = `currentUser=${JSON.stringify(data)}; path=/`

      toast({
        title: "Login successful",
        description: `Welcome back, ${data.name}!`,
      })

      // Wait for state updates before redirecting
      setTimeout(() => {
        if (data.role === 'admin') {
          router.push('/dashboard')
        } else {
          router.push('/user-panel')
        }
      }, 100)
    } catch (error) {
      toast({
        variant: 'destructive',
        title: "Login failed",
        description: error instanceof Error 
          ? error.message 
          : "Please check your credentials and try again.",
      })
      setCurrentUser(null)
      localStorage.removeItem('currentUser')
      document.cookie = 'currentUser=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT'
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 bg-white p-8 rounded-lg shadow-lg">
      <div className="space-y-2">
        <h1 className="text-2xl font-bold text-center text-gray-900">Login</h1>
        <p className="text-sm text-center text-gray-600">Enter your credentials to access the system</p>
      </div>

      <div className="space-y-4">
        <div>
          <Input
            type="text"
            placeholder="Username"
            value={formData.username}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            className="w-full"
            required
          />
        </div>
        
        <div>
          <Input
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            className="w-full"
            required
          />
        </div>

        <div className="flex items-center space-x-2">
          <Checkbox
            id="rememberMe"
            checked={formData.rememberMe}
            onCheckedChange={(checked) => 
              setFormData({ ...formData, rememberMe: checked as boolean })
            }
          />
          <label 
            htmlFor="rememberMe" 
            className="text-sm text-gray-600 cursor-pointer"
          >
            Remember me
          </label>
        </div>

        <Button 
          type="submit" 
          className="w-full"
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Logging in...
            </>
          ) : (
            'Login'
          )}
        </Button>
      </div>

      {/* Debug information */}
      <div className="mt-4 text-xs text-gray-500">
        <p>Available users:</p>
        <ul className="list-disc pl-5">
          <li>Admin: admin / admin123</li>
          <li>User: user1 / user123</li>
          <li>Viewer: viewer1 / viewer123</li>
        </ul>
      </div>
    </form>
  )
}
