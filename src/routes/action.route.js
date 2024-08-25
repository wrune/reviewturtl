// import { Router } from "express";
// import { octokitMiddleware } from "../middlewares/octokit.middleware.js";
// import { sendError, sendResponse } from "../utils/responseHandler.js";
// import { StatusCodes, ReasonPhrases } from "http-status-codes";

// const actionRouter = Router();

// actionRouter.post("/review", octokitMiddleware, async (req, res) => {
//   try {
//     console.log("Action request received");
//     const { octokit } = req;
//     const { pull_request } = req.body;
//     const { number } = pull_request;
//     // create a review comment.
//     await octokit.pulls.createReview({
//       owner: pull_request.base.repo.owner.login,
//       repo: pull_request.base.repo.name,
//       pull_number: number,
//       event: "APPROVE",
//     });

//     sendResponse(res, http.STATUS_CODES.OK, "PR approved successfully");
//   } catch (error) {
//     console.error("Error approving PR", error);
//     sendError(
//       res,
//       StatusCodes.INTERNAL_SERVER_ERROR,
//       ReasonPhrases.INTERNAL_SERVER_ERROR
//     );
//   }
// });

// actionRouter.post("/summerise", octokitMiddleware, async (req, res) => {
//   console.log("Action request received");
//   res.sendStatus(200);
// });

// export { actionRouter };
