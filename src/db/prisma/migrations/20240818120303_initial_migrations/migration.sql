-- CreateEnum
CREATE TYPE "Status" AS ENUM ('ACTIVE', 'INACTIVE');

-- CreateTable
CREATE TABLE "Installations" (
    "id" INTEGER NOT NULL,
    "githubAccount" TEXT NOT NULL,

    CONSTRAINT "Installations_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "pullRequests" (
    "id" TEXT NOT NULL,
    "prNumber" INTEGER NOT NULL,
    "repoName" TEXT NOT NULL,
    "Owner" TEXT NOT NULL,
    "installationId" INTEGER NOT NULL,
    "turtleStatus" "Status" NOT NULL,

    CONSTRAINT "pullRequests_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "pullRequests" ADD CONSTRAINT "pullRequests_installationId_fkey" FOREIGN KEY ("installationId") REFERENCES "Installations"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
