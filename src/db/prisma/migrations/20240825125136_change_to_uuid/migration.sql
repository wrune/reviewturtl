/*
  Warnings:

  - You are about to drop the `Installations` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `pullRequests` table. If the table is not empty, all the data it contains will be lost.

*/
-- CreateEnum
CREATE TYPE "status" AS ENUM ('ACTIVE', 'INACTIVE');

-- DropForeignKey
ALTER TABLE "pullRequests" DROP CONSTRAINT "pullRequests_installationId_fkey";

-- DropTable
DROP TABLE "Installations";

-- DropTable
DROP TABLE "pullRequests";

-- DropEnum
DROP TYPE "Status";

-- CreateTable
CREATE TABLE "installations" (
    "id" INTEGER NOT NULL,
    "account" TEXT NOT NULL,

    CONSTRAINT "installations_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "repo" (
    "id" TEXT NOT NULL,
    "repo_name" TEXT NOT NULL,
    "owner" TEXT NOT NULL,
    "default_branch" TEXT NOT NULL,
    "installation_id" INTEGER NOT NULL,

    CONSTRAINT "repo_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "pull_requests" (
    "id" TEXT NOT NULL,
    "pr_number" INTEGER NOT NULL,
    "repo_name" TEXT NOT NULL,
    "owner" TEXT NOT NULL,
    "installation_id" INTEGER NOT NULL,
    "turtle_status" "status" NOT NULL,

    CONSTRAINT "pull_requests_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "file_metadata" (
    "id" TEXT NOT NULL,
    "repo_id" TEXT NOT NULL,
    "file_path" TEXT NOT NULL,
    "is_indexed" BOOLEAN NOT NULL,

    CONSTRAINT "file_metadata_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "repo" ADD CONSTRAINT "repo_installation_id_fkey" FOREIGN KEY ("installation_id") REFERENCES "installations"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "pull_requests" ADD CONSTRAINT "pull_requests_installation_id_fkey" FOREIGN KEY ("installation_id") REFERENCES "installations"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "file_metadata" ADD CONSTRAINT "file_metadata_repo_id_fkey" FOREIGN KEY ("repo_id") REFERENCES "repo"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
