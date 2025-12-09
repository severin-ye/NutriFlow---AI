export interface MealEntry {
    id: string
    food: string
    calories: number
    protein: number
    carbs: number
    fat: number
    timestamp: number
    imageUrl: string
    date: string // YYYY-MM-DD format
}

export interface DailySummary {
    date: string
    totalCalories: number
    totalProtein: number
    totalCarbs: number
    totalFat: number
    meals: MealEntry[]
    mealCount: number
}

// Helper to format date as YYYY-MM-DD
export function formatDate(date: Date): string {
    return date.toISOString().split('T')[0]
}

// Helper to format time as HH:MM AM/PM
export function formatTime(timestamp: number): string {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Get meals from local storage
export function getMealsFromStorage(): MealEntry[] {
    if (typeof window === 'undefined') return []

    try {
        const stored = localStorage.getItem('meals')
        return stored ? JSON.parse(stored) : []
    } catch (e) {
        console.error('Failed to parse meals from storage', e)
        return []
    }
}

// Save meals to local storage
export function saveMealsToStorage(meals: MealEntry[]) {
    if (typeof window === 'undefined') return
    localStorage.setItem('meals', JSON.stringify(meals))
}

// Add a new meal
export function addMeal(meal: Omit<MealEntry, 'id' | 'timestamp' | 'date'>): MealEntry {
    const meals = getMealsFromStorage()
    const now = new Date()

    const newMeal: MealEntry = {
        ...meal,
        id: `meal_${now.getTime()}_${Math.random().toString(36).substr(2, 9)}`,
        timestamp: now.getTime(),
        date: formatDate(now)
    }

    meals.push(newMeal)
    saveMealsToStorage(meals)
    return newMeal
}

// Get meals for a specific date
export function getMealsByDate(date: string): MealEntry[] {
    const meals = getMealsFromStorage()
    return meals.filter(meal => meal.date === date)
}

// Get daily summary
export function getDailySummary(date: string): DailySummary {
    const meals = getMealsByDate(date)

    const summary: DailySummary = {
        date,
        totalCalories: 0,
        totalProtein: 0,
        totalCarbs: 0,
        totalFat: 0,
        meals,
        mealCount: meals.length
    }

    meals.forEach(meal => {
        summary.totalCalories += meal.calories
        summary.totalProtein += meal.protein
        summary.totalCarbs += meal.carbs
        summary.totalFat += meal.fat
    })

    return summary
}

// Get all dates that have meals
export function getAllMealDates(): string[] {
    const meals = getMealsFromStorage()
    const dates = new Set(meals.map(meal => meal.date))
    return Array.from(dates).sort().reverse()
}
