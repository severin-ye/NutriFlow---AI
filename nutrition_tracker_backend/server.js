import express from "express";
import cors from "cors";
import userRoutes from "./src/routes/analyze.js";
import authRoutes from "./src/routes/auth.js";
import mealsRoute from "./src/routes/meals.js";

const app = express();

app.use(cors({
    origin: "http://localhost:3000",
    methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allowedHeaders: ["Content-Type", "Authorization"],
    credentials: true,
}));

app.use(express.json({limit: "30mb"}));

// Routes
app.use("/analyze", userRoutes);
app.use("/auth", authRoutes);
app.use("/meals", mealsRoute);

const PORT = 4000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

