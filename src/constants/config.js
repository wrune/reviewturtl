import dotenv from "dotenv";
import fs from "fs";
dotenv.config();

const privateKey = fs.readFileSync("./rt.pem", "utf-8", (err, data) => {
  if (err) {
    console.error("Error reading file, add rt.pem file at root", err);
    return;
  }
  return data;
});

const config = {
  PORT: process.env.PORT || 3000,
  NODE_ENV: process.env.NODE_ENV || "development",
  GITHUB_APP_ID: process.env.GITHUB_APP_ID,
  GITHUB_PRIVATE_KEY: privateKey,
  WEBHOOK_PROXY_URL: process.env.WEBHOOK_PROXY_URL,
  TURTLE_API: process.env.TURTLE_API,
  TURTLE_API_VERSION: process.env.TURTLE_API_VERSION,
  DATABASE_URL: process.env.DATABASE_URL,
};
console.log("Environment config loaded!!");

export default config;
