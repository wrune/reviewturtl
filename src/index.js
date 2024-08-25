import express from "express";
import config from "./constants/config.js";
import SmeeClient from "smee-client";
import { webhookRouter } from "./routes/webhook.route.js";
// import { actionRouter } from "./routes/action.route.js";
import { errorHandler } from "./middlewares/errorHandler.middleware.js";

const app = express();
const port = process.env.PORT || 3000;

// Smee client setup
const smee = new SmeeClient({
  source: config.WEBHOOK_PROXY_URL,
  target: `http://localhost:${port}/webhook`,
  logger: console,
});

// Start smee client
const events = smee.start();

// Middleware to parse JSON payloads
app.use(
  express.json({
    verify: (req, res, buf, encoding) => {
      req.rawBody = buf.toString(encoding || "utf8");
    },
  })
);

// Routes
app.use("/webhook", webhookRouter);
// app.use("/action", actionRouter);

// Error handling middleware
app.use(errorHandler);

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

process.on("SIGINT", () => {
  console.log("Stopping smee client");
  events.close();
  process.exit();
});
