from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import shutil
from pathlib import Path
import tempfile
import os
from main import analyze_meal_from_image  # import your function from main.py

app = FastAPI(title="Nutrition Agent API")

# Enable CORS so your JS backend can call it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend/backend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_meal(file: UploadFile, meal_type: str = ""):
    """
    Endpoint to analyze a meal image.
    Accepts an image upload and optional meal_type.
    Returns JSON result from analyze_food.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Save uploaded file temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
            
        # Call your existing analyze_food function
        result = analyze_meal_from_image(tmp_path, meal_type)
        #with open("output.json", "w", encoding="utf-8") as f:
        #    json.dump(result, f, ensure_ascii=False, indent=4)# indent for pretty printing
        
        BASE_DIR = Path(__file__).resolve().parent

# Build the full path to meals.json dynamically
        meals_file = BASE_DIR / "ai_nutrition_agent/db/meals.json"

        with meals_file.open( "r", encoding="utf-8") as f:
           data = json.load(f)

# Get the most recent day
        latest_day = data['days'][-1]
        last_meal = latest_day['meals'][-1]  # Get the last meal of that day
        dish_array = [
            {
                "name": dish["name"],
                "calories": dish["nutrition_total"]["calories"],
                "carbs": dish["nutrition_total"]["carbs"],
                "protein": dish["nutrition_total"]["protein"],
                "fats": dish["nutrition_total"]["fat"]
            }
            for dish in last_meal["dishes"]
        ]
        return dish_array

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
