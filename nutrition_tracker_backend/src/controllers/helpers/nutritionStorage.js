import fs from "fs";
import path from "path";

const dataDir = path.join(process.cwd(), "data");
const nutritionFile = path.join(process.cwd(),"data", "nutritionData.json");

// Ensure data directory + file
export function ensureNutritionFile() {
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir);
    console.log("[INIT] Created /data folder");
  }

  if (!fs.existsSync(nutritionFile)) {
    fs.writeFileSync(nutritionFile, "{}");
    console.log("[INIT] Created empty nutritionData.json");
  }
}

// Read JSON
export function readNutritionData() {
  ensureNutritionFile();
  if (!fs.existsSync(nutritionFile)) return [];
  const data = fs.readFileSync(nutritionFile, "utf8");
  return JSON.parse(data || "[]");
}

// Save JSON
export function writeNutritionData(data) {
  ensureNutritionFile();
    console.log("Writing to:", path.resolve(nutritionFile));
  fs.writeFileSync(nutritionFile, JSON.stringify(data, null, 2));
}

// Add a new food entry
export function addNutritionEntry(userName, entry) {
  ensureNutritionFile();

  const data = readNutritionData();

  const date = new Date().toISOString().split("T")[0]; // YYYY-MM-DD
  const time = new Date().toTimeString().slice(0, 5);  // HH:MM
  if (!data[userName]) data[userName] = {};
  if (!data[userName][date]) data[userName][date] = {};
  if (!data[userName][date][time]) data[userName][date][time] = [];
  data[userName][date][time].push(entry);

  writeNutritionData(data);

}

