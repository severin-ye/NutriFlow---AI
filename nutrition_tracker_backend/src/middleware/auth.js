import jwt from "jsonwebtoken";

export function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Missing or invalid token" });
  }

  const token = authHeader.split(" ")[1];

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || "secret");

    // Attach email to req
    req.userEmail = decoded.email;

    next();
  } catch (error) {
    return res.status(401).json({ error: "Invalid or expired token" });
  }
}

