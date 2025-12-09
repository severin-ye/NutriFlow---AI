import express from "express";
import fs from"fs";
import path from "path";

const router = express.Router();

// Suppose you have your JSON stored in a file
const DATA_FILE = path.join(process.cwd(), "data", "nutritionData.json");

// GET /api/meals/:userId/:date
router.get("/:userId/:date", (req, res) => {
  try {
    const { userId, date } = req.params;
    const rawData = fs.readFileSync(DATA_FILE, "utf-8");
    const allData = JSON.parse(rawData);

    if (!allData[userId] || !allData[userId][date]) {
      return res.status(404).json({ error: "No data found" });
    }

    const mealsByTime = allData[userId][date];
    console.log(mealsByTime);
    // Flatten all dishes into one array, keep timestamp
    const formattedDishes = [];
    Object.entries(mealsByTime).forEach(([time, dishes]) => {
      dishes.forEach(dish => {
        formattedDishes.push({
          id: `${userId}_${date}_${time}_${dish.name}`,
          food: dish.name,
          calories: dish.calories,
          protein: dish.protein,
          carbs: dish.carbs,
          fat: dish.fats,
          timestamp: new Date(`${date}T${time}`).getTime(),
          image: dish.imageBase64 || null, // base64 image if exists
          date,
          time
        });
      });
    });

    // Return array sorted by timestamp
    formattedDishes.sort((a, b) => a.timestamp - b.timestamp);

    res.json({ success: true, meals: formattedDishes });
  } catch (err) {
    console.error("Get meals error:", err);
    res.status(500).json({ error: "Internal Server Error", details: err.message });
  }
});

export default router;

