'use client'

import { useRouter, usePathname } from 'next/navigation'
import { ArrowLeft, LogOut } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { useApp } from "@/contexts/AppContext"
import { useToast } from "@/components/ui/use-toast"
import { useEffect } from 'react'

export default function UserPanelLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const pathname = usePathname()
  const { currentUser, logout } = useApp()
  const { toast } = useToast()

  // Check if we're on a sensor detail page
  const isSensorDetailPage = pathname.startsWith('/user-panel/sensors/')

  useEffect(() => {
    // Check if user is logged in and has correct role
    if (!currentUser || (currentUser.role !== 'user' && currentUser.role !== 'viewer')) {
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
  if (!currentUser || (currentUser.role !== 'user' && currentUser.role !== 'viewer')) {
    return null
  }

  return (
    <div className="min-h-screen bg-white">
      <header className="bg-black text-white px-4 py-3 flex items-center justify-between">
        <h1 className="text-xl font-semibold">Water Quality Dashboard</h1>
        <Button 
          variant="ghost" 
          size="sm"
          onClick={handleLogout}
          className="text-white hover:text-gray-200"
        >
          Logout
        </Button>
      </header>

      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between mb-4">
          {isSensorDetailPage && (
            <div className="flex items-center gap-4">
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => router.push('/user-panel')}
                className="text-black hover:text-gray-700"
              >
                <ArrowLeft className="h-4 w-4 mr-1" />
                Back to Sensors
              </Button>
            </div>
          )}
          {isSensorDetailPage && (
            <Button 
              variant="outline"
              size="sm"
              onClick={() => router.push('/user-panel/historical-reports')}
              className="text-black hover:text-gray-700"
            >
              Historical Reports
            </Button>
          )}
        </div>

        <main>
          {children}
        </main>
      </div>
    </div>
  )
}
