import crypto from "crypto";
import { StatusCodes, ReasonPhrases } from "http-status-codes";

// Webhook verification middleware
const verifyWebhook = (req, res, next) => {
  const signature = req.headers["x-hub-signature-256"];

  if (!signature) {
    return res
      .status(StatusCodes.BAD_REQUEST)
      .send(`${ReasonPhrases.BAD_REQUEST}, No webhook signature provided`);
  }

  const hmac = crypto.createHmac("sha256", process.env.WEBHOOK_SECRET);
  const digest = Buffer.from(
    "sha256=" + hmac.update(req.rawBody).digest("hex"),
    "utf8"
  );
  const checksum = Buffer.from(signature, "utf8");

  if (
    checksum.length !== digest.length ||
    !crypto.timingSafeEqual(digest, checksum)
  ) {
    return res
      .status(StatusCodes.UNAUTHORIZED)
      .send(ReasonPhrases.UNAUTHORIZED);
  }

  next();
};

export { verifyWebhook };
