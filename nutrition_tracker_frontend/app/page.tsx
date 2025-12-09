"use client"

import { useState,useEffect } from "react"
import { useRouter } from "next/navigation"
import NutritionTracker from "@/components/nutrition-tracker"
import { Loader2, LogOut, BarChart3 } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function Home() {
  const router = useRouter()


  const [userName, setUserName] = useState("Guest");

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      try {
        const user = JSON.parse(storedUser) as { name?: string };
        if (user.name) setUserName(user.name);
      } catch {}
    }
  }, []);


  const handleLogout = () => {
    localStorage.removeItem("user")
    router.push("/auth")
  }

  return (
    <main className="min-h-screen relative">
      {/* Header buttons */}
      <div className="absolute top-4 right-4 z-50 flex gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => router.push("/summary")}
          className="rounded-full"
        >
          <BarChart3 className="w-4 h-4 mr-2" />
          View Summary
        </Button>

        <Button
          variant="outline"
          size="sm"
          onClick={handleLogout}
          className="rounded-full"
        >
          <LogOut className="w-4 h-4 mr-2" />
          Logout
        </Button>
      </div>

      {/* Welcome message */}
      <div className="absolute top-4 left-4 z-50">
        <p className="text-sm text-muted-foreground">
          Welcome, <span className="font-semibold text-foreground">{userName}</span>!
        </p>
      </div>

      <NutritionTracker />
    </main>
  )
}
