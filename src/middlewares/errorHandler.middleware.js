import logger from "../utils/logger.js";
import { StatusCodes, ReasonPhrases } from "http-status-codes";
import { sendError } from "../utils/responseHandler.js";

const errorHandler = (err, req, res, next) => {
  logger.error(`Unhandled error: ${err.message}`, { stack: err.stack });
  sendError(
    res,
    StatusCodes.INTERNAL_SERVER_ERROR,
    ReasonPhrases.INTERNAL_SERVER_ERROR
  );
};

export { errorHandler };
