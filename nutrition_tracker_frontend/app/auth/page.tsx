"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Sparkles, Loader2 } from "lucide-react"

type AuthMode = "login" | "signup"
const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function AuthPage() {
    const router = useRouter()
    const [mode, setMode] = useState<AuthMode>("login")
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState("")

    // Form state
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [name, setName] = useState("")
    const [age, setAge] = useState("")
    const [weight, setWeight] = useState("")
    const [height, setHeight] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError("")
        setIsLoading(true)
        console.log("test");

        try {
            const endpoint = mode === "login" ? `${API_URL}/auth/login` : `${API_URL}/auth/signup`
            const body = mode === "login"
                ? { email, password }
                : { email, password, name, age: parseInt(age), weight: parseFloat(weight), height: parseFloat(height) }

            const response = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            })

            const data = await response.json()

            if (!response.ok) {
                console.log(data);
                setError(data.message || "Something went wrong")
                setIsLoading(false)
                return
            }

            console.log(data);

            // Store user in localStorage
            localStorage.setItem("token", data.token);

            localStorage.setItem("user", JSON.stringify(data.user))

            // Redirect to main app
            router.push("/")
        } catch (err) {
            setError("Network error. Please try again.")
            setIsLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-b from-background to-secondary/20 flex items-center justify-center p-4">
            <div className="w-full max-w-md">
                {/* Header */}
                <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/10 mb-4">
                        <Sparkles className="w-8 h-8 text-primary" />
                    </div>
                    <h1 className="text-4xl font-bold mb-2">{"NutriScan AI"}</h1>
                    <p className="text-muted-foreground">
                        {mode === "login" ? "Welcome back!" : "Create your account"}
                    </p>
                </div>

                <Card className="overflow-hidden shadow-xl">
                    {/* Tab Switcher */}
                    <div className="grid grid-cols-2 gap-0 border-b">
                        <button
                            onClick={() => setMode("login")}
                            className={`py-4 text-center font-semibold transition-colors ${mode === "login"
                                    ? "bg-primary text-primary-foreground"
                                    : "bg-muted text-muted-foreground hover:bg-muted/80"
                                }`}
                        >
                            Login
                        </button>
                        <button
                            onClick={() => setMode("signup")}
                            className={`py-4 text-center font-semibold transition-colors ${mode === "signup"
                                    ? "bg-primary text-primary-foreground"
                                    : "bg-muted text-muted-foreground hover:bg-muted/80"
                                }`}
                        >
                            Sign Up
                        </button>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="p-6 space-y-4">
                        {error && (
                            <div className="p-3 rounded-lg bg-destructive/10 text-destructive text-sm">
                                {error}
                            </div>
                        )}

                        {mode === "signup" && (
                            <div>
                                <label className="block text-sm font-medium mb-2">Name</label>
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    required
                                    className="w-full px-4 py-2 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary"
                                    placeholder="John Doe"
                                />
                            </div>
                        )}

                        <div>
                            <label className="block text-sm font-medium mb-2">Email</label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                className="w-full px-4 py-2 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary"
                                placeholder="you@example.com"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-2">Password</label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                className="w-full px-4 py-2 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary"
                                placeholder="••••••••"
                            />
                        </div>

                        {mode === "signup" && (
                            <>
                                <div className="grid grid-cols-3 gap-3">
                                    <div>
                                        <label className="block text-sm font-medium mb-2">Age</label>
                                        <input
                                            type="number"
                                            value={age}
                                            onChange={(e) => setAge(e.target.value)}
                                            required
                                            min="1"
                                            max="150"
                                            className="w-full px-4 py-2 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary"
                                            placeholder="25"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium mb-2">Weight (kg)</label>
                                        <input
                                            type="number"
                                            value={weight}
                                            onChange={(e) => setWeight(e.target.value)}
                                            required
                                            min="1"
                                            step="0.1"
                                            className="w-full px-4 py-2 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary"
                                            placeholder="70"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium mb-2">Height (cm)</label>
                                        <input
                                            type="number"
                                            value={height}
                                            onChange={(e) => setHeight(e.target.value)}
                                            required
                                            min="1"
                                            step="0.1"
                                            className="w-full px-4 py-2 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary"
                                            placeholder="170"
                                        />
                                    </div>
                                </div>
                            </>
                        )}

                        <Button
                            type="submit"
                            size="lg"
                            className="w-full rounded-xl"
                            disabled={isLoading}
                        >
                            {isLoading ? (
                                <>
                                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                                    {mode === "login" ? "Logging in..." : "Creating account..."}
                                </>
                            ) : (
                                <>{mode === "login" ? "Login" : "Sign Up"}</>
                            )}
                        </Button>
                    </form>
                </Card>

                <p className="text-center text-sm text-muted-foreground mt-4">
                    {mode === "login" ? "Don't have an account? " : "Already have an account? "}
                    <button
                        onClick={() => setMode(mode === "login" ? "signup" : "login")}
                        className="text-primary hover:underline font-medium"
                    >
                        {mode === "login" ? "Sign up" : "Login"}
                    </button>
                </p>
            </div>
        </div>
    )
}
