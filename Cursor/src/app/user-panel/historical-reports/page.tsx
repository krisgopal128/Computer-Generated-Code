'use client'

import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { ArrowLeft } from 'lucide-react'

export default function HistoricalReportsPage() {
  const router = useRouter()

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button 
          variant="ghost" 
          size="sm"
          onClick={() => router.back()}
          className="text-black hover:text-gray-700"
        >
          <ArrowLeft className="h-4 w-4 mr-1" />
          Back
        </Button>
        <h2 className="text-3xl font-bold tracking-tight">Historical Reports</h2>
      </div>

      <div className="border rounded-lg p-6">
        <p className="text-center text-muted-foreground">
          Historical reports functionality coming soon...
        </p>
      </div>
    </div>
  )
} 