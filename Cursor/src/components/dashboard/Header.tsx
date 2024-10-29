'use client'

import { Bell } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function Header() {
  return (
    <header className="h-16 border-b border-gray-200 bg-white px-6 flex items-center justify-between">
      <h1 className="text-xl font-semibold text-gray-800">Dashboard</h1>
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon">
          <Bell className="h-5 w-5" />
        </Button>
        <span className="text-sm text-gray-600">Admin</span>
      </div>
    </header>
  )
}
