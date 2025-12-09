"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell,
    Legend
} from "recharts"
import { ChevronLeft, Calendar, Flame, Utensils, Droplet, Wheat } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
    getDailySummary,
    getAllMealDates,
    formatDate,
    formatTime,
    type DailySummary as DailySummaryType,
    type MealEntry
} from "@/types/meal"

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];
const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function DailySummary() {
    const router = useRouter()
    const [selectedDate, setSelectedDate] = useState<string>(formatDate(new Date()))
    const [summary, setSummary] = useState<DailySummaryType | null>(null)
    const [availableDates, setAvailableDates] = useState<string[]>([])

    useEffect(() => {
        // Load available dates
        const dates = getAllMealDates()
        setAvailableDates(dates)

        // If no dates available, use today
        if (dates.length === 0) {
            setAvailableDates([formatDate(new Date())])
        }
    }, [])

    useEffect(() => {
        // Load summary for selected date
        const dailySummary = getDailySummary(selectedDate)
        setSummary(dailySummary)
    }, [selectedDate]);
    useEffect(() => {
            loadDemoData();
    },[]);

    const loadDemoData = async () => {
        //const today = formatDate(new Date())
        const userString = localStorage.getItem("user");

        if (userString) {
            const user = JSON.parse(userString).email; // Convert JSON string back to object
        const today = new Date();
        const date = today.toISOString().split('T')[0];
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/meals/${user}/${date}`)
        const data = await response.json()

        const demoMeals: MealEntry[] = data ? data.meals : [
            {
                id: "demo_1",
                food: "Oatmeal with Berries",
                calories: 350,
                protein: 12,
                carbs: 60,
                fat: 6,
                timestamp: Date.now() - 28800000,
                imageUrl: "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=500",
                date: today
            },
            {
                id: "demo_2",
                food: "Grilled Chicken Salad",
                calories: 450,
                protein: 45,
                carbs: 15,
                fat: 20,
                timestamp: Date.now() - 14400000,
                imageUrl: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500",
                date: today
            },
            {
                id: "demo_3",
                food: "Salmon with Asparagus",
                calories: 550,
                protein: 40,
                carbs: 10,
                fat: 35,
                timestamp: Date.now() - 3600000,
                imageUrl: "https://images.unsplash.com/photo-1467003909585-2f8a7270028d?w=500",
                date: today
            }
        ]
        localStorage.setItem('meals', JSON.stringify(demoMeals))
        } 
    }

    if (!summary) return null

    // Prepare data for charts
    const macroData = [
        { name: 'Protein', value: summary.totalProtein},
        { name: 'Carbs', value: summary.totalCarbs },
        { name: 'Fat', value: summary.totalFat },
    ].filter(item => item.value > 0);

    const calorieData = summary.meals.map(meal => ({
        name: meal.food.length > 15 ? meal.food.substring(0, 15) + '...' : meal.food,
        calories: meal.calories
    }));

    return (
        <div className="min-h-screen bg-background p-4 md:p-8 space-y-8">
            {/* Header */}
            <div className="flex items-center justify-between max-w-5xl mx-auto">
                <Button
                    variant="ghost"
                    onClick={() => router.push('/')}
                    className="gap-2"
                >
                    <ChevronLeft className="w-4 h-4" />
                    Back to Tracker
                </Button>
                <h1 className="text-2xl font-bold">Daily Summary</h1>
                <div className="w-24" /> {/* Spacer for centering */}
            </div>

            <div className="max-w-5xl mx-auto space-y-8">
                {/* Date Selector */}
                <div className="flex items-center gap-4 overflow-x-auto pb-2 scrollbar-hide">
                    {availableDates.map(date => (
                        <Button
                            key={date}
                            variant={selectedDate === date ? "default" : "outline"}
                            onClick={() => setSelectedDate(date)}
                            className="whitespace-nowrap"
                        >
                            {date === formatDate(new Date()) ? "Today" : new Date(date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
                        </Button>
                    ))}
                </div>

                {/* Summary Stats Cards */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Calories</CardTitle>
                            <Flame className="h-4 w-4 text-orange-500" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{summary.totalCalories}</div>
                            <p className="text-xs text-muted-foreground">{summary.mealCount} meals</p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Protein</CardTitle>
                            <Utensils className="h-4 w-4 text-blue-500" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{parseFloat(summary.totalProtein.toFixed(2))}g</div>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Carbs</CardTitle>
                            <Wheat className="h-4 w-4 text-yellow-500" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{parseFloat(summary.totalCarbs.toFixed(2))}g</div>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Fat</CardTitle>
                            <Droplet className="h-4 w-4 text-red-500" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{parseFloat(summary.totalFat.toFixed(2))}g</div>
                        </CardContent>
                    </Card>
                </div>

                {/* Charts Section */}
                {summary.mealCount > 0 ? (
                    <div className="grid md:grid-cols-2 gap-8">
                        {/* Calorie Chart */}
                        <Card>
                            <CardHeader>
                                <CardTitle>Calories per Meal</CardTitle>
                            </CardHeader>
                            <CardContent className="h-[300px]">
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={calorieData}>
                                        <CartesianGrid strokeDasharray="3 3" />
                                        <XAxis dataKey="name" />
                                        <YAxis />
                                        <Tooltip />
                                        <Bar dataKey="calories" fill="#f97316" radius={[4, 4, 0, 0]} />
                                    </BarChart>
                                </ResponsiveContainer>
                            </CardContent>
                        </Card>

                        {/* Macro Chart */}
                        <Card>
                            <CardHeader>
                                <CardTitle>Macro Distribution</CardTitle>
                            </CardHeader>
                            <CardContent className="h-[300px]">
                                <ResponsiveContainer width="100%" height="100%">
                                    <PieChart>
                                        <Pie
                                            data={macroData}
                                            cx="50%"
                                            cy="50%"
                                            innerRadius={60}
                                            outerRadius={80}
                                            fill="#8884d8"
                                            paddingAngle={5}
                                            dataKey="value"
                                        >
                                            {macroData.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                            ))}
                                        </Pie>
                                        <Tooltip />
                                        <Legend />
                                    </PieChart>
                                </ResponsiveContainer>
                            </CardContent>
                        </Card>
                    </div>
                ) : (
                    <div className="text-center py-12 bg-muted/30 rounded-xl">
                        <p className="text-muted-foreground mb-4">No meals recorded for this day.</p>
                        <div className="flex gap-4 justify-center">
                            <Button
                                variant="outline"
                                onClick={loadDemoData}
                            >
                                Load Demo Data
                            </Button>
                            <Button
                                onClick={() => router.push('/')}
                            >
                                Start Tracking
                            </Button>
                        </div>
                    </div>
                )}

                {/* Meal History List */}
                {summary.mealCount > 0 && (
                    <div className="space-y-4">
                        <h2 className="text-xl font-semibold">Meal History</h2>
                        <div className="grid gap-4">
                            {summary.meals.map((meal) => (
                                <Card key={meal.id} className="overflow-hidden">
                                    <div className="flex items-center gap-4 p-4">
                                        <div className="h-16 w-16 rounded-lg overflow-hidden bg-muted shrink-0">
                                        {/*<img
                                                src={meal.image}
                                                alt={meal.food}
                                                className="h-full w-full object-cover"
                                            /> */}
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <div className="flex items-center justify-between mb-1">
                                                <h3 className="font-semibold truncate">{meal.food}</h3>
                                                <span className="text-sm text-muted-foreground">{formatTime(meal.timestamp)}</span>
                                            </div>
                                            <div className="flex items-center gap-4 text-sm text-muted-foreground">
                                                <span className="font-medium text-primary">{meal.calories} kcal</span>
                                                <span className="hidden sm:inline">|</span>
                                                <div className="flex gap-3 text-xs sm:text-sm">
                                                    <span>P: {meal.protein}g</span>
                                                    <span>C: {meal.carbs}g</span>
                                                    <span>F: {meal.fat}g</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </Card>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
