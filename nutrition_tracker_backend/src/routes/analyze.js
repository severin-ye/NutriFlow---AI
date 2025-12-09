import { Router } from "express";
import pkg from "multer";
import { analyzeImage } from "../controllers/analyzeController.js";
import { authMiddleware } from "../middleware/auth.js";

const multer = pkg;


const router = Router();
const upload = multer({ storage: multer.memoryStorage() });

// Temporarily disabled auth for testing
router.post("/", upload.single("image"), analyzeImage);

export default router;

