# MSE-2 Practical Examination — Final Submission Report
**Course:** Software Engineering & DevOps (AI310B) — Morning Shift  
**Student Name:** Shubham Kumar  
**University Roll Number:** 2400291520242  
**Registration / Student ID:** 202401100300243  
**Section:** D  
**Branch:** B.Tech CSE (AI) / CSE-AIML  
**College:** KIET Group of Institutions, Delhi-NCR  
**GitHub Profile:** [https://github.com/ishubhamkumar005](https://github.com/ishubhamkumar005)  
**Starter Repository:** [https://github.com/atindeRR/MSE-2-SSED-Morning](https://github.com/atindeRR/MSE-2-SSED-Morning)  
**Personal Fork:** [https://github.com/ishubhamkumar005/MSE-2-SSED-Morning](https://github.com/ishubhamkumar005/MSE-2-SSED-Morning)  
**Official Pull Request:** [https://github.com/atindeRR/MSE-2-SSED-Morning/pull/4](https://github.com/atindeRR/MSE-2-SSED-Morning/pull/4)  
**Target Branch:** `main`  
**Date:** 18 November 2026  

---

## 1. Project Overview

This project completes the end-to-end containerization, orchestration, data persistence, caching, and CI/CD validation for **TaskFlow**, a multi-tier task management application.

The application architecture includes:
- **Frontend:** React 18 SPA built with Vite, served via an **Nginx 1.27 Alpine** reverse proxy.
- **Backend:** Node.js 20 Express REST API running as unprivileged user (`USER 1000`).
- **Database:** PostgreSQL 16 Alpine with persistent named volume `postgres_data` and auto-initialization script `init.sql`.
- **Caching:** Redis 7 Alpine implementing Cache-Aside with Write-Invalidation and 30-second TTL.
- **CI/CD:** Automated GitHub Actions workflows for static linting (Hadolint), integration testing (Jest/Supertest), Docker Hub image publishing, and deployment verification.

---

## 2. Requirements Completed

- [x] **Repository Analysis & Setup:** Fully analyzed directory structure, routes, database schemas, and workflows. Created [PROJECT_ANALYSIS.md](file:///C:/Users/Shubham%20Kumar/Downloads/MSE-2-SSED-Morning-main/PROJECT_ANALYSIS.md).
- [x] **Frontend Dockerfile:** Multi-stage build (`node:20-alpine` builder $\rightarrow$ `nginx:1.27-alpine` production server). Reverse proxy configured for `/api/` and `/health`. Validated with Hadolint (0 warnings).
- [x] **Backend Dockerfile:** Lean `node:20-alpine` image with production dependencies only (`npm install --omit=dev`), `USER 1000` non-root execution, and correct entrypoint. Validated with Hadolint (0 warnings).
- [x] **Docker Compose (`docker-compose.yml`):** Fully orchestrates all 4 services with internal bridge networking (`taskflow-net`), port mappings (`8080:80`, `3000:3000`), health checks on all dependencies, and named volume persistence.
- [x] **Deployment Compose (`docker-compose.deploy.yml`):** Pure image-based deployment referencing Docker Hub published images with zero `build:` directives.
- [x] **Environment & Security:** Secured `.env` file, comprehensive `.env.example`, `.gitignore` ensuring zero secret leaks.
- [x] **PostgreSQL Persistence:** Verified that database records survive complete `docker compose down` and recreation.
- [x] **Redis Caching:** Verified that `GET /api/tasks` populates cache and returns `source: 'redis-cache'`, and mutating operations invalidate cache.
- [x] **Automated Test Suite:** 12/12 Jest integration test cases passed (`tests/api.test.js`).
- [x] **Viva Preparation Guide:** Created [VIVA_QUESTIONS.md](file:///C:/Users/Shubham%20Kumar/Downloads/MSE-2-SSED-Morning-main/VIVA_QUESTIONS.md) containing 55 detailed questions and answers in beginner-friendly Hinglish.
- [x] **Practical Commands Reference:** Created [PRACTICAL_COMMANDS.md](file:///C:/Users/Shubham%20Kumar/Downloads/MSE-2-SSED-Morning-main/PRACTICAL_COMMANDS.md) for live exam demonstration.
- [x] **PDF Submission Documentation:** Generated official document [2400291520242_SHUBHAM_KUMAR.pdf](file:///C:/Users/Shubham%20Kumar/Downloads/MSE-2-SSED-Morning-main/2400291520242_SHUBHAM_KUMAR.pdf).
- [x] **Official Pull Request:** Created [PR #4: DOCKER-EXAM | 2400291520242 | Shubham Kumar | D](https://github.com/atindeRR/MSE-2-SSED-Morning/pull/4) against instructor's repository.

---

## 3. Files Created and Modified

| File | Status | Description |
|---|---|---|
| `frontend/Dockerfile` | Created / Configured | Multi-stage build (Vite + Nginx) |
| `backend/Dockerfile` | Created / Configured | Production Node.js 20 Alpine (USER 1000) |
| `docker-compose.yml` | Created | Local build multi-container orchestration |
| `docker-compose.deploy.yml` | Created | Published image-only deployment configuration |
| `.env.example` | Updated | Added complete template environment variables |
| `.env` | Created (Ignored) | Local environment runtime configuration |
| `submission.json` | Created | Evaluation identity file for automated grading |
| `PROJECT_ANALYSIS.md` | Created | In-depth technical architecture analysis |
| `VIVA_QUESTIONS.md` | Created | 55 comprehensive viva questions & answers |
| `PRACTICAL_COMMANDS.md` | Created | Practical exam demonstration command cheatsheet |
| `generate_pdf.py` | Created | Python ReportLab PDF document generator |
| `2400291520242_SHUBHAM_KUMAR.pdf`| Generated | Official 2-page examination submission document |
| `FINAL_SUBMISSION_REPORT.md` | Created | Final submission audit report |
| `deployment-evidence/` | Created | Genuine test logs, curl responses, and container tables |

---

## 4. Docker Images & IDs

| Image Name | Tag | Image ID / Digest | Size | Purpose |
|---|---|---|---|---|
| `taskflow-backend` | `local` | `5b6462b86a4f` | ~165 MB | Local backend API service |
| `taskflow-frontend` | `local` | `f4914b647347` | ~24.8 MB | Local Nginx React static server |
| `postgres` | `16-alpine` | `a2d17f5b24d5` | ~380 MB | Relational database |
| `redis` | `7-alpine` | `dfed3a5d50b9` | ~45 MB | In-memory cache |

---

## 5. Live Containers & Status

| Container Name | Service | Ports | Health Status | Runtime Status |
|---|---|---|---|---|
| `mse-2-ssed-morning-main-frontend-1` | `frontend` | `0.0.0.0:8080->80/tcp` | Running | Up |
| `mse-2-ssed-morning-main-backend-1` | `backend` | `0.0.0.0:3000->3000/tcp` | Healthy | Up (healthy) |
| `mse-2-ssed-morning-main-postgres-1` | `postgres` | `5432/tcp` | Healthy | Up (healthy) |
| `mse-2-ssed-morning-main-redis-1` | `redis` | `6379/tcp` | Healthy | Up (healthy) |

---

## 6. URLs & Endpoints

- **Frontend Application UI:** [http://localhost:8080/](http://localhost:8080/)
- **Backend Health Check:** [http://localhost:3000/health](http://localhost:3000/health)
- **Frontend Reverse Proxy Health:** [http://localhost:8080/health](http://localhost:8080/health)
- **Official Pull Request:** [https://github.com/atindeRR/MSE-2-SSED-Morning/pull/4](https://github.com/atindeRR/MSE-2-SSED-Morning/pull/4)
- **Student GitHub Fork:** [https://github.com/ishubhamkumar005/MSE-2-SSED-Morning](https://github.com/ishubhamkumar005/MSE-2-SSED-Morning)

---

## 7. PostgreSQL Persistence Results

Verified via direct SQL query after full stack teardown (`docker compose down`) and restart (`docker compose up -d`):
```text
 count 
-------
     1
(1 row)
```
Named volume `postgres_data` guarantees that customer accounts and task records are persisted across container lifecycles.

---

## 8. Redis Caching Results

Verified via Jest automated integration test suite:
- First fetch (`TC07`): Populates Redis cache with 30s TTL (`source: 'postgres'` or `'redis-cache'`).
- Second fetch (`TC08`): Served directly from memory (`source: 'redis-cache'`).
- Update/Delete (`TC09`, `TC11`): Successfully invokes `redis.del(cacheKey)` for immediate cache invalidation.

---

## 9. Cleanup Instructions

When practical demonstration is finished:
```bash
# Gracefully stop and tear down containers
docker compose down

# If a complete reset including volume deletion is required
docker compose down -v --remove-orphans
```
