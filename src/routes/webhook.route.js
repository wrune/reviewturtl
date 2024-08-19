import { Router } from "express";
import { sendResponse } from "../utils/responseHandler.js";
import { handleWebhookEvent } from "../controllers/webhook.controller.js";
import { StatusCodes, ReasonPhrases } from "http-status-codes";
import { asyncHandler } from "../utils/asyncHandler.js";

const webhookRouter = Router();

webhookRouter.post(
  "/",
  asyncHandler(async (req, res) => {
    const event = req.headers["x-github-event"];
    const installationId = req.body.installation?.id;
    await handleWebhookEvent(req.body, event, installationId);
    sendResponse(
      res,
      StatusCodes.OK,
      `${ReasonPhrases.OK}: Webhook processed successfully`
    );
  })
);

export { webhookRouter };
