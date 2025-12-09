import fs from "fs";
import path from "path";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import dotenv from "dotenv";
dotenv.config();

const dataDir = path.join(process.cwd(), "data");
const usersFile = path.join(process.cwd(), "data", "users.json");

function ensureStorage() {
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir);
    console.log("[INIT] Created /data folder");
  }

  if (!fs.existsSync(usersFile)) {
    fs.writeFileSync(usersFile, "[]");
    console.log("[INIT] Created empty users.json");
  }
}

// Load all users
function loadUsers() {
  ensureStorage();
  if (!fs.existsSync(usersFile)) return [];
  const data = fs.readFileSync(usersFile, "utf8");
  return JSON.parse(data || "[]");
}

function saveUsers(data) {
  ensureStorage();
  fs.writeFileSync(usersFile, JSON.stringify(data, null, 2));
}

// ======================== SIGN UP =========================

export const signup = async (req , res) => {
    const { email, password, name, age, weight, height } = req.body;

    if (!email || !password || !name || !age || !weight || !height) {
        return res.status(400).json({ message: "Missing required fields" });
    }

    const users = loadUsers();

    if (users.some(u => u.email === email)) {
        return res.status(400).json({ message: "Email already used" });
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const newUser= { email, hashedPassword, name, age, weight, height };
    users.push(newUser);

    const token = jwt.sign(
        { email: newUser.email },
        process.env.JWT_SECRET,
        { expiresIn: "7d" }
     );
    saveUsers(users);

    return res.status(201).json({ 
        message: "User registered successfully",
        token,
        user:{
        email: newUser.email,
        name: newUser.name,
        age: newUser.age,
        weight: newUser.weight,
        height: newUser.height
        } });
};

// ======================== LOGIN =========================

export const login = async (req, res) => {
    const { email, password } = req.body;

    if (!email || !password) {
        return res.status(400).json({ message: "Email and password required" });
    }

    const users = loadUsers();
    const user = users.find(u => u.email === email);

    if (!user) {
        return res.status(401).json({ message: "Invalid email or password" });
    }
    const match = await bcrypt.compare(password, user.hashedPassword);
    if (!match) {
      return res.status(400).json({ error: "Invalid credentials" });
    }

    const token = jwt.sign(
        { email: user.email },
        process.env.JWT_SECRET,
        { expiresIn: "7d" }
     );

    return res.status(200).json({
        message: "Login successful",
        token,
        user:{
        email: user.email,
        name: user.name,
        age: user.age,
        weight: user.weight,
        height: user.height
        }
    });
};

