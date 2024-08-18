import dotenv from "dotenv";

dotenv.config();

const config = {
  PORT: process.env.PORT || 3000,
  NODE_ENV: process.env.NODE_ENV || "development",
  GITHUB_APP_ID: process.env.GITHUB_APP_ID,
  GITHUB_PRIVATE_KEY: process.env.GITHUB_PRIVATE_KEY,
  WEBHOOK_PROXY_URL: process.env.WEBHOOK_PROXY_URL,
  TURTLE_API: process.env.TURTLE_API,
  DATABASE_URL: process.env.DATABASE_URL,
};

export default config;
