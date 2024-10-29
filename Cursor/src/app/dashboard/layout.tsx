'use client'

import { useRouter } from 'next/navigation'
import Sidebar from '@/components/dashboard/Sidebar'
import Header from '@/components/dashboard/Header'
import { Button } from "@/components/ui/button"
import { LogOut } from 'lucide-react'
import { useApp } from "@/contexts/AppContext"
import { useToast } from "@/components/ui/use-toast"
import { useEffect } from 'react'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const { logout, currentUser } = useApp()
  const { toast } = useToast()

  useEffect(() => {
    // Check if user is logged in and is admin
    if (!currentUser || currentUser.role !== 'admin') {
      router.push('/')
    }
  }, [currentUser, router])

  const handleLogout = () => {
    logout()
    toast({
      title: "Logged out successfully",
      description: "You have been logged out of the system.",
    })
    router.push('/')
  }

  // Don't render anything while checking authentication
  if (!currentUser || currentUser.role !== 'admin') {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Sidebar />
      <div className="pl-64">
        <div className="flex items-center justify-between bg-white px-6 py-4 border-b">
          <Header />
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">
              Welcome, {currentUser.name}
            </span>
            <Button 
              variant="outline" 
              size="sm"
              onClick={handleLogout}
              className="flex items-center gap-2"
            >
              <LogOut className="h-4 w-4" />
              Logout
            </Button>
          </div>
        </div>
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
