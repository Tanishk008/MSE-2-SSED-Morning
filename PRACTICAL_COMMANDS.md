# MSE-2 DevOps Practical Exam — Essential Command Reference
**Course:** Software Engineering & DevOps (AI310B)  
**Student:** Shubham Kumar | **GitHub:** [ishubhamkumar005](https://github.com/ishubhamkumar005)  
**Project:** TaskFlow Containerization & Deployment

---

## 1. DOCKER ENVIRONMENT CHECK

```bash
# Check Docker Engine version
docker --version

# Check Docker Compose version
docker compose version

# Check Docker Daemon info (OS, CPUs, Memory, Storage Driver)
docker info

# Check current Docker context
docker context show
```
*Explanation:* Verify that Docker Engine is running and ready for container execution.

---

## 2. STATIC VALIDATION & LINTING (HADOLINT)

```bash
# Validate Frontend Dockerfile using Hadolint
Get-Content frontend\Dockerfile | docker run --rm -i hadolint/hadolint

# Validate Backend Dockerfile using Hadolint
Get-Content backend\Dockerfile | docker run --rm -i hadolint/hadolint
```
*Explanation:* Hadolint parses Dockerfiles against industry-standard Dockerfile best practices (e.g., pinned base image tags, numeric user UID `USER 1000`). Exit code 0 means zero linting violations.

---

## 3. DOCKER COMPOSE CONFIGURATION VALIDATION

```bash
# Validate local build Compose syntax and environment resolution
docker compose config --quiet

# Validate deployment Compose file (must have 0 build: directives)
docker compose -f docker-compose.deploy.yml config --quiet

# Verify deployment file has no build directives
Select-String -Pattern "^\s+build:" docker-compose.deploy.yml
```
*Explanation:* Checks YAML indentation, schema validity, service links, and environment variables without starting containers.

---

## 4. LOCAL BUILD & MULTI-CONTAINER STARTUP

```bash
# Build frontend and backend images locally from source
docker compose build

# Start all 4 services in detached mode with dependencies and health checks
docker compose up -d

# Verify all containers are running and healthy
docker compose ps

# View real-time aggregated logs of all 4 services
docker compose logs

# View logs of a specific service
docker compose logs backend
docker compose logs frontend
docker compose logs postgres
docker compose logs redis
```
*Explanation:* Builds `taskflow-backend:local` and `taskflow-frontend:local`, spins up `postgres` and `redis`, waits for their health checks, and boots the backend and Nginx frontend.

---

## 5. HEALTH AND CONNECTIVITY VERIFICATION

```bash
# Check Backend Health Endpoint (checks PostgreSQL SELECT 1 & Redis ping)
curl.exe -i http://localhost:3000/health

# Check Frontend Nginx Reverse Proxy to Health Endpoint
curl.exe -i http://localhost:8080/health

# Check Frontend Web UI accessibility
curl.exe -I http://localhost:8080/
```
*Explanation:* Verifies that Express API is listening on port 3000, Nginx is proxying `/health` and `/api/` from port 8080 to backend:3000, and static React SPA bundle is served.

---

## 6. JEST AUTOMATED INTEGRATION TESTS

```bash
# Run 12 comprehensive integration tests against containerized stack
cd tests
$env:BASE_URL="http://localhost:3000"
$env:NODE_OPTIONS="--experimental-vm-modules"
npm test
cd ..
```
*Explanation:* Executes tests covering User Registration, Duplicate Email Rejection (409), JWT Login, Authenticated Task Creation, Redis Cache Population, Redis Cache Hit (`source: redis-cache`), Task Status Update, Cache Invalidation, and Deletion.

---

## 7. POSTGRESQL DATA PERSISTENCE DEMONSTRATION

```bash
# 1. Inspect records currently in PostgreSQL
docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT id, name, email, created_at FROM users;"

# 2. Stop and remove containers and network (WITHOUT deleting volumes)
docker compose down

# 3. Start fresh containers
docker compose up -d

# 4. Query database again — verify data is preserved
docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT id, name, email, created_at FROM users;"
```
*Explanation:* Proves that database records survive container recreation because PostgreSQL stores its data inside the Docker named volume `postgres_data`.

---

## 8. DOCKER HUB IMAGE TAGGING & PUBLISHING

```bash
# 1. Log in to Docker Hub
docker login -u YOUR_DOCKERHUB_USERNAME

# 2. Build and Tag Backend image
docker build -t YOUR_DOCKERHUB_USERNAME/taskflow-backend:latest ./backend
docker build -t YOUR_DOCKERHUB_USERNAME/backend:latest ./backend

# 3. Build and Tag Frontend image
docker build -t YOUR_DOCKERHUB_USERNAME/taskflow-frontend:latest ./frontend
docker build -t YOUR_DOCKERHUB_USERNAME/frontend:latest ./frontend

# 4. Push Backend images to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/taskflow-backend:latest
docker push YOUR_DOCKERHUB_USERNAME/backend:latest

# 5. Push Frontend images to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/taskflow-frontend:latest
docker push YOUR_DOCKERHUB_USERNAME/frontend:latest
```
*Explanation:* Publishes production images to public Docker Hub registry so they can be pulled and run anywhere without source code.

---

## 9. DEPLOYMENT FROM PUBLISHED DOCKER HUB IMAGES

```bash
# 1. Pull images from Docker Hub using deployment Compose file
docker compose -f docker-compose.deploy.yml pull

# 2. Launch stack using published registry images
docker compose -f docker-compose.deploy.yml up -d

# 3. Verify deployment containers
docker compose -f docker-compose.deploy.yml ps

# 4. Verify deployment health
curl.exe http://localhost:3000/health
```
*Explanation:* Simulates production server deployment where no local source code exists and containers run directly from remote Docker Hub images.

---

## 10. GIT & GITHUB ACTIONS COMMANDS

```bash
# Check git status
git status

# Stage all files
git add .

# Commit changes
git commit -m "Implement Docker containerization, Docker Compose, and CI/CD pipelines"

# Push to your personal fork
git push origin main
```
*Explanation:* Pushes commits to GitHub fork, automatically triggering GitHub Actions `cd.yml` pipeline.

---

## 11. CLEANUP COMMANDS

```bash
# Stop and remove containers from local compose
docker compose down

# Stop and remove containers and delete volumes (complete teardown)
docker compose down -v --remove-orphans

# Stop deployment compose stack
docker compose -f docker-compose.deploy.yml down -v --remove-orphans

# Remove unused Docker images
docker image prune -f
```
*Explanation:* Clean up resources and stop background daemon tasks after evaluation.
