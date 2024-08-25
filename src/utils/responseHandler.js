import logger from "./logger.js";

const sendResponse = (res, statusCode, data) => {
  logger.info(`Sending response: ${statusCode}`, { data });
  return res.status(statusCode).json(data);
};

const sendError = (res, statusCode, message) => {
  logger.error(`Error: ${statusCode} - ${message}`);
  return res.status(statusCode).json({ error: message });
};

export { sendResponse, sendError };
