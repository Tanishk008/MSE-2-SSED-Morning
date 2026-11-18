# TaskFlow — Project Analysis & Containerization Architecture
**Course:** Software Engineering and DevOps (AI310B) — MSE-2 Practical Exam  
**Student:** Shubham Kumar (GitHub: [ishubhamkumar005](https://github.com/ishubhamkumar005))  
**Repository:** [https://github.com/ishubhamkumar005/MSE-2-SSED-Morning](https://github.com/ishubhamkumar005/MSE-2-SSED-Morning)  
**Starter Repository:** [https://github.com/atindeRR/MSE-2-SSED-Morning](https://github.com/atindeRR/MSE-2-SSED-Morning)  

---

## 1. Project Overview

TaskFlow is a production-style, multi-tier task management application designed for DevOps practical evaluation. It demonstrates full-stack containerization, multi-container orchestration, microservice communication, database persistence, distributed caching, image registry publishing, and automated CI/CD validation.

The system allows users to:
1. Register and authenticate using JWT (JSON Web Tokens) with salted bcrypt passwords.
2. Create, retrieve, update status of, and delete tasks.
3. Cache task listings in Redis for high-speed retrieval (with 30-second TTL and automatic cache invalidation upon task modifications).
4. Persist user records and task items permanently in PostgreSQL.
5. Access the user interface via an Nginx reverse proxy that routes browser traffic and API calls seamlessly.

---

## 2. Directory Structure

```text
MSE-2-SSED-Morning/
├── .github/
│   └── workflows/
│       ├── cd.yml                  # CD pipeline: build, push to Docker Hub, pull, deploy & test
│       └── ci.yml                  # CI pipeline: validate Dockerfiles (hadolint), build, test persistence & API
├── backend/
│   ├── db/
│   │   └── init.sql               # Database schema initialization script (users, tasks, index)
│   ├── src/
│   │   ├── app.js                 # Express application, routes (/health, /api/auth, /api/tasks)
│   │   ├── auth.js                # JWT verification middleware
│   │   ├── config.js              # Environment variable parsing and defaults
│   │   ├── db.js                  # PostgreSQL pool and retry connection logic
│   │   ├── redis.js               # Redis client connection and retry logic
│   │   └── server.js              # Server entry point (starts after DB & Redis ready, handles SIGTERM/SIGINT)
│   ├── .dockerignore              # Ignore node_modules, .env, tests, npm logs
│   ├── Dockerfile                 # Multi-stage/lean Node.js production image
│   └── package.json               # Backend dependencies (express, pg, redis, bcryptjs, jsonwebtoken, cors)
├── frontend/
│   ├── src/
│   │   ├── main.jsx               # React main component (Auth UI, Task management UI, cache indicator)
│   │   └── style.css              # Frontend CSS styling
│   ├── .dockerignore              # Ignore node_modules, dist, .env, npm logs
│   ├── Dockerfile                 # Multi-stage build (Node.js builder -> Nginx Alpine server)
│   ├── index.html                 # Single Page Application HTML root
│   ├── nginx.conf                 # Nginx reverse proxy configuration (/ -> static, /api/ -> backend:3000)
│   ├── package.json               # Frontend dependencies (react, react-dom, vite)
│   └── vite.config.js             # Vite configuration
├── tests/
│   ├── api.test.js                # Jest test suite (12 test cases covering health, auth, CRUD, cache)
│   ├── jest.config.js             # Jest configuration for ES Modules
│   └── package.json               # Test dependencies (jest, supertest)
├── .env.example                   # Template environment variables
├── .gitignore                     # Git ignore rules (node_modules, .env, dist, coverage)
├── docker-compose.yml             # Local development orchestration (builds from source)
├── docker-compose.deploy.yml      # Deployment orchestration (pulls published Docker Hub images)
├── PROJECT_ANALYSIS.md            # Detailed technical analysis and architecture documentation
└── README.md                      # Examination problem statement and instructions
```

---

## 3. Technology Stack

| Layer | Technology | Version / Base Image | Purpose |
|---|---|---|---|
| **Frontend** | React.js + Vite | `node:20-alpine` (build) & `nginx:1.27-alpine` (serve) | Client SPA UI with reverse proxy |
| **Backend** | Node.js + Express.js | `node:20-alpine` | REST API, Business logic, Auth, Middleware |
| **Database** | PostgreSQL | `postgres:16-alpine` | Relational persistent data store |
| **Caching** | Redis | `redis:7-alpine` | In-memory key-value cache for task listings |
| **Orchestration**| Docker & Docker Compose | Compose Specification v2 | Multi-container coordination & networking |
| **CI/CD** | GitHub Actions | Ubuntu Latest Runner | Automated build, linting, testing, and deployment |
| **Image Registry**| Docker Hub | Official Registry | Public repository hosting for container images |

---

## 4. Frontend Architecture

- **Framework:** React 18 built with Vite bundler.
- **Serving Mechanism:** Nginx 1.27 Alpine.
- **Port:** Exposes container port `80`, mapped to host port `8080`.
- **Reverse Proxy Routing (`nginx.conf`):**
  - `/` -> Serves static React production bundle from `/usr/share/nginx/html` with SPA fallback (`try_files $uri $uri/ /index.html`).
  - `/api/` -> Proxies requests directly to `http://backend:3000/api/` inside Docker bridge network.
  - `/health` -> Proxies to `http://backend:3000/health`.
- **Benefits:** Eliminates CORS issues in production, hides internal container topology, and provides ultra-fast static asset delivery with minimal memory footprint (~15-25 MB RAM).

---

## 5. Backend Architecture

- **Runtime:** Node.js 20 with native ES Modules (`"type": "module"`).
- **Framework:** Express.js 4.
- **Container Port:** `3000` (mapped to host port `3000`).
- **Security:**
  - Salted hash password storage via `bcryptjs` (salt rounds: 10).
  - Stateless authentication via `jsonwebtoken` (JWT) with 8-hour expiry.
  - Runs as unprivileged user (`USER 1000` / `node`) adhering to Docker security best practices.
- **Resilience:**
  - `waitForDatabase()`: Retries PostgreSQL connectivity up to 30 times with 2-second backoff.
  - `connectRedis()`: Retries Redis connectivity up to 30 times with 1-second backoff.
  - Graceful shutdown handlers for `SIGTERM` and `SIGINT` closing HTTP server and Redis connection.

### API Endpoints
- `GET /health`: Comprehensive health check validating PostgreSQL (`SELECT 1`) and Redis (`redis.ping()`).
- `POST /api/auth/register`: Creates new user account. Rejects duplicate emails (HTTP 409).
- `POST /api/auth/login`: Authenticates credentials and returns JWT bearer token.
- `GET /api/tasks`: Returns tasks for authenticated user. Checks Redis cache key `tasks:user:<id>`; on cache miss, queries PostgreSQL, populates Redis cache with 30s TTL, and returns tasks.
- `POST /api/tasks`: Creates a task, invalidates the user's Redis cache, returns created task.
- `PATCH /api/tasks/:id`: Updates task status (`Pending`, `In Progress`, `Completed`), invalidates Redis cache.
- `DELETE /api/tasks/:id`: Deletes task and invalidates Redis cache.

---

## 6. PostgreSQL Configuration

- **Image:** `postgres:16-alpine`
- **Port:** `5432` (internal container port; host port exposure optional/restricted for security)
- **Database Name:** `taskflow`
- **Default User:** `taskflow_user`
- **Initialization:** Mounts `./backend/db/init.sql` to `/docker-entrypoint-initdb.d/01-init.sql:ro`. Executes table creation for `users` and `tasks` and indexes on first startup.
- **Persistence:** Dedicated Docker named volume `postgres_data` mounted to `/var/lib/postgresql/data` ensuring data survives container restart, stop, or removal.
- **Health Check:** `pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}` with 5s interval, 5s timeout, and 10 retries.

---

## 7. Redis Configuration

- **Image:** `redis:7-alpine`
- **Port:** `6379` (internal container port)
- **Connection URL:** `redis://redis:6379`
- **Caching Strategy:** Cache-Aside with Write-Invalidation:
  - Cache Key: `tasks:user:<userId>`
  - Time To Live (TTL): 30 seconds (`EX: 30`)
  - Invalidation: Any mutating operation (`POST /api/tasks`, `PATCH /api/tasks/:id`, `DELETE /api/tasks/:id`) issues `redis.del(cacheKey)` ensuring strict cache consistency.
- **Health Check:** `redis-cli ping` with 5s interval, 3s timeout, and 10 retries.

---

## 8. Port Mapping & Networking

| Service | Container Port | Host Port | Protocol | Access |
|---|---|---|---|---|
| **frontend** | 80 | 8080 | HTTP | Public (Browser UI) |
| **backend** | 3000 | 3000 | HTTP | Public (API & Health Check) |
| **postgres** | 5432 | 5432 (optional) | TCP | Internal Docker Network |
| **redis** | 6379 | 6379 (optional) | TCP | Internal Docker Network |

- **Network:** User-defined bridge network `taskflow-net` enables automatic DNS resolution by service name (`postgres`, `redis`, `backend`, `frontend`).

---

## 9. Environment Variables

| Variable | Default / CI Value | Purpose |
|---|---|---|
| `POSTGRES_DB` | `taskflow` | PostgreSQL database name |
| `POSTGRES_USER` | `taskflow_user` | PostgreSQL database user |
| `POSTGRES_PASSWORD` | Secure random / provided via secret | PostgreSQL user password |
| `DATABASE_URL` | `postgresql://taskflow_user:password@postgres:5432/taskflow` | Connection string for Node.js `pg` Pool |
| `REDIS_URL` | `redis://redis:6379` | Connection string for Redis client |
| `JWT_SECRET` | Strong secret string | Secret key for signing and verifying JWT tokens |
| `PORT` | `3000` | HTTP port on which Express server listens |
| `DOCKERHUB_USERNAME`| Student's Docker Hub handle | Used for pulling images in `docker-compose.deploy.yml` |

---

## 10. Application Communication Diagram

```
+-----------------------------------------------------------------------+
|                             HOST MACHINE                              |
|                                                                       |
|   Browser (User)                 Automated Test Suite / CI Runner     |
|   http://localhost:8080          http://localhost:3000                |
+---------+-----------------------------------+-------------------------+
          |                                   |
          | Port 8080:80                      | Port 3000:3000
          v                                   v
+-----------------------------------------------------------------------+
|                    DOCKER BRIDGE NETWORK (taskflow-net)               |
|                                                                       |
|  +--------------------+             +------------------------------+  |
|  |     frontend       |             |           backend            |  |
|  |  (Nginx 1.27)      |--proxy_pass-->  (Express Node.js 20)       |  |
|  |  Serves React SPA  |  /api/      |   Listens on port 3000       |  |
|  +--------------------+             +---------------+--------------+  |
|                                                     |                 |
|                                 +-------------------+---------------+ |
|                                 |                                   | |
|                                 v (DNS: postgres:5432)              v (DNS: redis:6379)
|                       +--------------------+             +-------------------+
|                       |      postgres      |             |       redis       |
|                       |   (PostgreSQL 16)  |             |     (Redis 7)     |
|                       +---------+----------+             +-------------------+
|                                 |                                     |
+---------------------------------|-------------------------------------+
                                  v
                        [ postgres_data Volume ]
```

---

## 11. Docker Implementation Plan

1. **Frontend Dockerfile:**
   - Multi-stage build:
     - Stage 1 (`build`): `node:20-alpine`, copy `package*.json`, run `npm install`, copy source, execute `npm run build`.
     - Stage 2 (production): `nginx:1.27-alpine`, copy `nginx.conf` to `/etc/nginx/conf.d/default.conf`, copy build output from Stage 1 to `/usr/share/nginx/html`.
   - Passes Hadolint with zero warnings.
2. **Backend Dockerfile:**
   - Base image: `node:20-alpine`.
   - Copy `package*.json`, install production dependencies (`npm install --omit=dev`).
   - Copy `src/` and `db/`.
   - Run as unprivileged user (`USER 1000`).
   - Passes Hadolint with zero warnings.
3. **docker-compose.yml (Local Build):**
   - Configures `frontend`, `backend`, `postgres`, `redis`.
   - Includes health checks on all dependencies with `depends_on: { condition: service_healthy }`.
   - Uses named volume `postgres_data` for data persistence.
4. **docker-compose.deploy.yml (Registry Deployment):**
   - Pure image-based deployment without `build:` directives.
   - Images: `${DOCKERHUB_USERNAME}/taskflow-frontend:latest` and `${DOCKERHUB_USERNAME}/taskflow-backend:latest`.

---

## 12. CI/CD Workflow Analysis

- **`ci.yml` (Pull Request Evaluation):**
  - Triggered on PRs to `main`.
  - Runs Hadolint linting on both Dockerfiles.
  - Builds containers via `docker compose build`.
  - Spins up stack and waits for backend `/health` and frontend HTTP 200.
  - Runs Jest integration tests (`tests/api.test.js`).
  - Verifies data persistence across container recreations.
- **`cd.yml` (Continuous Delivery & Deployment Verification):**
  - Triggered on push to `main`.
  - Authenticates to Docker Hub using GitHub Secrets (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`).
  - Builds and tags backend & frontend images using Buildx and pushes to Docker Hub.
  - Validates `docker-compose.deploy.yml` (ensures zero `build:` directives).
  - Pulls published images from Docker Hub and starts services.
  - Runs health checks and Jest API test suite against live deployed containers.
