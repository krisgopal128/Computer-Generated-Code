'use client'

import { useState } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { useToast } from "@/components/ui/use-toast"
import { X } from 'lucide-react'

interface HistoricalReportProps {
  isOpen: boolean
  onClose: () => void
  sensorId: string
  sensorName: string
}

export default function HistoricalReportDialog({ 
  isOpen, 
  onClose,
  sensorId,
  sensorName
}: HistoricalReportProps) {
  const { toast } = useToast()
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [parameters, setParameters] = useState({
    Salinity: false,
    DO: false,
    pH: false,
    Temp: false,
    Cond: false,
    Depth: false,
    Turbidity: false
  })

  const handleExport = async () => {
    if (!startDate || !endDate) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Please select both start and end dates.",
      })
      return
    }

    const selectedParams = Object.entries(parameters)
      .filter(([_, selected]) => selected)
      .map(([param]) => param)

    if (selectedParams.length === 0) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Please select at least one parameter.",
      })
      return
    }

    try {
      // Format the CSV data
      const headers = ['Timestamp', ...selectedParams]
      const csvContent = headers.join(',') + '\n'
      
      // TODO: Fetch historical data from API
      // const data = await fetchHistoricalData(sensorId, startDate, endDate, selectedParams)
      
      // Create and download the CSV file
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', `${sensorName}_historical_data.csv`)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)

      toast({
        title: "Success",
        description: "Historical data exported successfully.",
      })
      onClose()
    } catch (error) {
      console.error('Error exporting data:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to export historical data. Please try again.",
      })
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <div className="flex items-center justify-between">
            <DialogTitle>Historical Report</DialogTitle>
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>
        </DialogHeader>
        
        <div className="space-y-6 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Start Date</label>
              <input
                type="datetime-local"
                className="w-full rounded-md border border-input px-3 py-2"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">End Date</label>
              <input
                type="datetime-local"
                className="w-full rounded-md border border-input px-3 py-2"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Select Parameters</label>
            <div className="grid grid-cols-2 gap-4">
              {Object.keys(parameters).map((param) => (
                <div key={param} className="flex items-center space-x-2">
                  <Checkbox
                    id={param}
                    checked={parameters[param as keyof typeof parameters]}
                    onCheckedChange={(checked) => 
                      setParameters(prev => ({ ...prev, [param]: checked }))
                    }
                  />
                  <label 
                    htmlFor={param}
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    {param}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <Button 
            className="w-full"
            onClick={handleExport}
          >
            Export CSV
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
} 