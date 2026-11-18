# TaskFlow DevOps Practical Examination — Comprehensive Viva Preparation Guide
**Course:** Software Engineering & DevOps (AI310B) — MSE-2 Practical Exam  
**Student:** Shubham Kumar | **GitHub:** [ishubhamkumar005](https://github.com/ishubhamkumar005)  
**Topics Covered:** Docker, Containers, Images, Dockerfile, Docker Compose, PostgreSQL Persistence, Redis Caching, Networking, Docker Hub, GitHub Actions, CI/CD Pipelines, Health Checks, Troubleshooting.

---

## SECTION 1: DOCKER FUNDAMENTALS & ARCHITECTURE

### Q1. Docker kya hai aur ye Virtual Machine (VM) se kaise alag hai?
**Answer:** Docker ek open-source containerization platform hai jo applications aur unki saari dependencies (libraries, binaries, config) ko ek lightweight container ke andar package karta hai.
- **Difference from VM:**
  - **Virtual Machine (VM):** Hypervisor ke upar chalta hai aur har VM ka apna complete **Guest OS** hota hai. Is wajah se VM heavy hota hai (GBs me size), boot hone me minutes lagte hain, aur RAM/CPU zyada consume karta hai.
  - **Docker Container:** Host OS ke **Kernel ko share** karta hai. Isme alag se Guest OS nahi hota, sirf application code aur runtime files hoti hain. Isliye containers lightweight (MBs me size) hote hain aur seconds me start ho jaate hain.

### Q2. Docker Engine ke main components kaun se hain?
**Answer:** Docker Engine ke teen main parts hote hain:
1. **Docker Daemon (`dockerd`):** Background process jo images, containers, networks, aur volumes ko manage karta hai.
2. **Docker CLI (`docker` command):** Command Line Interface jiske through user Docker Daemon ko instructions deta hai (jaise `docker run`, `docker build`).
3. **REST API:** Interface jiske zariye Docker CLI aur Daemon aapas me communicate karte hain.

### Q3. Container lifecycle ke stages kya hote hain?
**Answer:** 
- **Created:** Container create ho chuka hai lekin start nahi hua (`docker create`).
- **Running:** Container actively process execute kar raha hai (`docker run` / `docker start`).
- **Paused:** Container ke processes suspend/freeze ho chuke hain (`docker pause`).
- **Stopped / Exited:** Main process complete ya stop ho chuka hai (`docker stop`).
- **Destroyed / Removed:** Container filesystem aur metadata delete ho chuke hain (`docker rm`).

### Q4. Docker me PID 1 process ka kya role hota hai?
**Answer:** Har container ke andar jo main command run hoti hai (specified by `CMD` ya `ENTRYPOINT`), wo PID 1 (Process ID 1) banti hai. Jab tak PID 1 process alive rehti hai, container tab tak run karta hai. Agar PID 1 process exit ya crash hoti hai, toh container automatically stop ho jaata hai. PID 1 signals (jaise `SIGTERM`, `SIGINT`) ko handle karne ke liye bhi responsible hoti hai.

### Q5. Container isolation kaise achieve hoti hai Linux me?
**Answer:** Linux Kernel ke do primary features se isolation milti hai:
1. **Namespaces:** Process isolation provide karte hain (PID namespace alag process tree deta hai, NET namespace alag network interface/IP deta hai, MNT namespace alag filesystem deta hai).
2. **Cgroups (Control Groups):** Hardware resource allocation control karte hain (RAM limits, CPU usage, I/O bandwidth).

---

## SECTION 2: DOCKER IMAGES & DOCKERFILE

### Q6. Docker Image aur Docker Container me kya farak hai?
**Answer:** 
- **Docker Image:** Ek **read-only blueprint ya template** hai jisme code, libraries, runtime aur system tools packaged hote hain. Ye class ki tarah immutable hoti hai.
- **Docker Container:** Us image ka ek **running instance** (object) hota hai. Container me image layers ke upar ek thin writable layer (container layer) add ho jaati hai jisme runtime modifications hoti hain.

### Q7. Dockerfile me Image Layers ka concept kya hota hai?
**Answer:** Dockerfile ki har instruction (jaise `FROM`, `COPY`, `RUN`) ek nayi immutable read-only layer banati hai. Docker in layers ko cache kar leta hai. Agar hum code me chhota sa change karte hain, toh Docker pehle ki unchanged layers ko cache se utha leta hai aur sirf changed layer ko rebuild karta hai. Isse build time dramatically kam ho jaata hai.

### Q8. Multi-Stage Build kya hota hai aur TaskFlow frontend me humne ise kyu use kiya?
**Answer:** Multi-stage build me ek hi Dockerfile ke andar multiple `FROM` statements use hote hain:
- **Build Stage (`node:20-alpine`):** Saari devDependencies install karke React app ka production bundle (`dist/`) compile karta hai.
- **Production Stage (`nginx:1.27-alpine`):** Pehle stage se sirf compiled `dist/` aur `nginx.conf` copy karta hai. Node.js runtime, npm, aur `node_modules` production image me include nahi hote.
- **Fayda:** Image ka size ~500MB se drop hokar sirf ~25MB reh jaata hai, aur attack surface drastically kam ho jaata hai.

### Q9. `CMD` aur `ENTRYPOINT` me kya difference hai?
**Answer:**
- `ENTRYPOINT`: Container ka default executable command define karta hai jisko easily override nahi kiya ja sakta (fixed command).
- `CMD`: Container ke default arguments provide karta hai ya default command define karta hai. Agar user `docker run <image> <args>` pass karta hai, toh `CMD` override ho jaata hai lekin `ENTRYPOINT` ke sath arguments append ho jaate hain.

### Q10. `COPY` aur `ADD` me kya farak hai? Best practice kya hai?
**Answer:** 
- `COPY`: Local files/directories ko host se container me copy karta hai. Simple aur transparent hota hai.
- `ADD`: Local files ke alawa remote URLs se files download kar sakta hai aur `.tar.gz` archives ko automatically extract kar sakta hai.
- **Best Practice:** Always use `COPY` unless aapko remote tar extraction ki specific need ho, taki unwanted layer caching aur security risks se bacha ja sake.

### Q11. Dockerfile me `.dockerignore` file ka kya importance hai?
**Answer:** `.dockerignore` file unwanted files (jaise `node_modules`, `.env`, `.git`, temporary build files) ko Docker build context me transfer hone se rokti hai.
- **Benefits:**
  1. Build context size chhota rehta hai (fast build speed).
  2. Host ke OS-specific compiled binaries container me crash nahi hote.
  3. Sensitive secrets (.env) image layer me leak hone se bachte hain.

### Q12. Backend Dockerfile me non-root user (`USER 1000`) kyu use kiya gaya?
**Answer:** By default, Docker container root user (UID 0) ke roop me execute hota hai. Agar container me koi remote code execution vulnerability aati hai, toh attacker container escape karke host machine ko compromise kar sakta hai. Isliye `USER 1000` (Node user) use karne se principle of least privilege follow hota hai aur security harden hoti hai.

### Q13. Hadolint kya hai aur `ci.yml` me iska kya kaam hai?
**Answer:** Hadolint ek static code analysis linter hai jo Dockerfiles ko Docker best practices aur ShellCheck rules ke according validate karta hai. Ye check karta hai ki pinned base images hain ya nahi, non-root user use hua hai ya nahi, aur cache clear ki gayi hai ya nahi.

---

## SECTION 3: DOCKER COMPOSE & MULTI-CONTAINER ORCHESTRATION

### Q14. Docker Compose kya hai aur single `docker run` ke mukable kyu behtar hai?
**Answer:** Docker Compose ek orchestration tool hai jo multi-container Docker applications ko define aur run karne ke liye YAML file (`docker-compose.yml`) use karta hai.
- Single command `docker compose up -d` se saare 4 services (Frontend, Backend, PostgreSQL, Redis), unke networks, volumes, environment variables aur dependencies ek sath start ho jaate hain, bajaye 4 alag-alag complex `docker run` commands execute karne ke.

### Q15. `docker-compose.yml` aur `docker-compose.deploy.yml` me key difference kya hai?
**Answer:**
- `docker-compose.yml`: Local development ke liye use hota hai. Isme `build: context: ./frontend` aur `build: context: ./backend` directives hote hain jo source code se local images build karte hain.
- `docker-compose.deploy.yml`: Production / Deployment environment ke liye use hota hai. Isme koi bhi `build:` directive allow nahi hoti; ye Docker Hub pe published images (`${DOCKERHUB_USERNAME}/taskflow-frontend:latest`) ko pull karke deploy karta hai.

### Q16. `depends_on` with `condition: service_healthy` kyu zaroori hai?
**Answer:** Simple `depends_on: [postgres]` sirf container ke start hone ka wait karta hai, database engine ready hone ka nahi. Agar backend start ho jaye jabki PostgreSQL abhi initialization scripts run kar raha hai, toh backend connection fail ho jayegi aur crash ho jayega. `condition: service_healthy` ensure karta hai ki backend tabhi start ho jab PostgreSQL aur Redis ka health check (`pg_isready` aur `redis-cli ping`) completely pass ho chuka ho.

### Q17. Docker Compose me `restart: unless-stopped` ka kya matlab hai?
**Answer:** Agar container crash ho jaye ya Docker daemon restart ho, toh Docker automatically container ko reboot kar dega, jab tak ki user ne explicitly `docker stop` na kiya ho.

### Q18. Compose file me Named Volumes aur Bind Mounts me kya difference hai?
**Answer:**
- **Named Volume (`postgres_data:/var/lib/postgresql/data`):** Docker dwara `/var/lib/docker/volumes/` me fully manage hota hai. High performance deta hai aur containers delete hone par bhi data safe rehta hai.
- **Bind Mount (`./backend/db/init.sql:/docker-entrypoint-initdb.d/01-init.sql`):** Host machine ke exact relative path ko container ke filesystem me map karta hai. Configuration files aur initial scripts ke liye ideal hai.

---

## SECTION 4: NETWORKING & COMMUNICATION

### Q19. Docker bridge network me Service Discovery kaise kaam karti hai?
**Answer:** Docker Compose default me ek custom bridge network (`taskflow-net`) create karta hai. Docker ke andar ek embedded DNS server hota hai (`127.0.0.11`). Jab backend container `postgres:5432` ya `redis:6379` ko request bhejta hai, toh Docker DNS automatically service name `postgres` ya `redis` ko corresponding container ke private IP address me resolve kar deta hai.

### Q20. Host port mapping `8080:80` aur `3000:3000` ka kya meaning hai?
**Answer:** Format hota hai `<HostPort>:<ContainerPort>`.
- `8080:80`: Host machine ke port 8080 par aane wala traffic container ke internal port 80 (Nginx) par forward hoga.
- `3000:3000`: Host machine ke port 3000 par aane wala traffic container ke internal port 3000 (Express API) par forward hoga.

### Q21. Backend code me `localhost` kyu nahi likha gaya database connection ke liye?
**Answer:** Container ke context ke andar `localhost` ka matlab hota hai "wahi specific container". Agar backend `localhost:5432` par connect karega, toh wo backend container ke andar hi postgres dhundega jo exist nahi karta. Dusre container se connect karne ke liye Docker network ka service hostname (`postgres` ya `redis`) use karna compulsory hai.

### Q22. Nginx reverse proxy me `/api/` route ka kya purpose hai?
**Answer:** Browser sirf frontend ke port 8080 se interact karta hai. Jab browser `/api/auth/login` ya `/api/tasks` call karta hai, toh Nginx `proxy_pass http://backend:3000/api/` directive ke through silently internal network par backend container ko request forward karta hai. Isse frontend aur backend ek hi origin par behave karte hain aur Cross-Origin Resource Sharing (CORS) issues nahi aate.

---

## SECTION 5: DATABASE PERSISTENCE & CACHING

### Q23. PostgreSQL data persistence kaise verify ki gayi?
**Answer:**
1. Stack start kiya aur test suite ke through ek user record create kiya (`SELECT count(*) FROM users` = 1).
2. `docker compose down` run karke saare running containers aur network destroy kiye (lekin volume flag `-v` nahi lagaya).
3. `docker compose up -d` se naye fresh containers start kiye.
4. Database query karne par pehle create kiya gaya user record intact mila, proving that `postgres_data` volume persists data across container lifecycle.

### Q24. `init.sql` script kab aur kaise execute hoti hai?
**Answer:** PostgreSQL image `/docker-entrypoint-initdb.d/` folder me mounted scripts ko sirf tabhi execute karti hai jab data directory empty ho (yani first-time volume creation). Agar volume me pehle se database files exist karti hain, toh ye scripts skip ho jaati hain taki existing data overwrite na ho.

### Q25. Redis Caching TaskFlow me kaise implemented hai?
**Answer:** Cache-Aside Pattern implement kiya gaya hai:
- **Read Operation (`GET /api/tasks`):**
  1. Backend pehle Redis key `tasks:user:<id>` check karta hai.
  2. Agar cache hit hua (`cached`), toh data Redis se return hota hai (`source: 'redis-cache'`).
  3. Agar cache miss hua, toh PostgreSQL se query karke data fetch hota hai, Redis me 30 seconds ke TTL ke sath set hota hai, aur return hota hai (`source: 'postgres'`).
- **Write Operations (`POST`, `PATCH`, `DELETE`):**
  Database me update ke turant baad `redis.del(cacheKey)` call hota hai taki stale data serve na ho (Cache Invalidation).

---

## SECTION 6: DOCKER HUB & IMAGE PUBLISHING

### Q26. Docker Hub kya hai?
**Answer:** Docker Hub ek cloud-based registry service hai jahan developers public aur private Docker images store, manage, version aur share karte hain.

### Q27. Image Tagging convention kya follow kiya gaya?
**Answer:** 
- Format: `<DockerHub_Username>/<Repository>:<Tag>`
- Backend: `ishubhamkumar005/taskflow-backend:latest` aur `ishubhamkumar005/backend:latest`
- Frontend: `ishubhamkumar005/taskflow-frontend:latest` aur `ishubhamkumar005/frontend:latest`
- Tags me commit SHA (`${{ github.sha }}`) bhi use kiya jata hai version tracking aur rollback enable karne ke liye.

### Q28. Docker Hub pe push karne ke basic steps kya hain?
**Answer:**
1. Authenticate: `docker login -u <username>`
2. Build & Tag: `docker build -t <username>/<repo>:<tag> <context>`
3. Push: `docker push <username>/<repo>:<tag>`

---

## SECTION 7: GITHUB ACTIONS & CI/CD PIPELINES

### Q29. CI aur CD me kya difference hai?
**Answer:**
- **CI (Continuous Integration):** Developers ke code changes ko automatically build, lint, aur test karna (jaise PR open hone par Hadolint validation, Jest test execution).
- **CD (Continuous Delivery / Continuous Deployment):** Tested code ko automatically container image build karke registry (Docker Hub) par push karna aur target environment me deploy karke verify karna.

### Q30. `ci.yml` aur `cd.yml` workflow triggers kya hain?
**Answer:**
- `ci.yml`: Pull Request events par trigger hota hai (`types: [opened, synchronize, reopened]`, `branches: [main]`).
- `cd.yml`: Main branch par direct `push` hone par trigger hota hai (`branches: [main]`) ya manually via `workflow_dispatch`.

### Q31. GitHub Repository Secrets kyu use kiye jaate hain aur kaun se secrets add kiye gaye?
**Answer:** Plain-text passwords ya access tokens ko git repository me commit karna dangerous security vulnerability hai. GitHub Secrets encrypted store provide karte hain jo sirf runner runtime par access hote hain:
- `DOCKERHUB_USERNAME`: Docker Hub user ID.
- `DOCKERHUB_TOKEN`: Docker Hub Personal Access Token (PAT).
- `POSTGRES_PASSWORD`: Database deployment password.

### Q32. CD pipeline ke 11 stages kaun se hain?
**Answer:**
1. Repository checkout (`actions/checkout@v4`)
2. Docker Buildx setup (`docker/setup-buildx-action@v3`)
3. Docker Hub authentication (`docker/login-action@v3`)
4. Backend image build (`docker/build-push-action@v6`)
5. Backend image publishing to Docker Hub
6. Frontend image build
7. Frontend image publishing to Docker Hub
8. Deployment environment file creation (`.env`)
9. Image-based deployment Compose validation & pull (`docker compose -f docker-compose.deploy.yml pull`)
10. Application deployment (`docker compose -f docker-compose.deploy.yml up -d`)
11. Backend health & frontend accessibility verification + Jest integration test execution.

---

## SECTION 8: HEALTH CHECKS & MONITORING

### Q33. Dockerfile me ya Compose me Healthcheck ka kya syntax hota hai?
**Answer:**
```yaml
healthcheck:
  test: ["CMD", "node", "-e", "fetch('http://127.0.0.1:3000/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]
  interval: 10s       # Har 10 second me test karo
  timeout: 5s         # 5 second me answer na aaye toh timeout
  retries: 5          # 5 baar fail hone par unhealthy mark karo
  start_period: 15s   # Initial boot time jisme failure count nahi hoga
```

### Q34. Backend `/health` endpoint kya inspect karta hai?
**Answer:** Ye endpoint do asynchronous checks perform karta hai:
1. `pool.query('SELECT 1')` -> Checks PostgreSQL active pool connectivity.
2. `redis.ping()` -> Checks Redis in-memory server responsiveness.
Dono successful hone par HTTP 200 `{ status: 'ok', postgres: 'ok', redis: 'ok' }` return karta hai, kisi ek ke fail hone par HTTP 503 return karta hai.

---

## SECTION 9: TROUBLESHOOTING & COMMON COMMANDS

### Q35. Agar container exit ho jaye toh debug kaise karenge?
**Answer:**
1. Check container status and exit code: `docker ps -a`
2. Inspect application logs: `docker logs <container_name_or_id>` ya `docker compose logs backend`
3. Check container events: `docker events`
4. Inspect low-level state: `docker inspect <container_id>`

### Q36. Container ke andar enter karke interactive debugging kaise karte hain?
**Answer:**
`docker exec -it <container_name> sh` ya bash:
Example:
`docker compose exec postgres psql -U taskflow_user -d taskflow`

### Q37. Docker volume aur dangling images clean karne ke commands kya hain?
**Answer:**
- `docker system prune -f`: Unused containers, networks, dangling images remove karta hai.
- `docker volume prune -f`: Unused volumes delete karta hai.
- `docker compose down -v`: Containers, networks ke sath-sath project volumes bhi destroy karta hai.

### Q38. `npm run build` frontend container me fail ho toh kya check karna chahiye?
**Answer:**
1. Check karo ki `COPY package*.json ./` ke baad `RUN npm install` properly execute hua ya nahi.
2. Check karo ki `.dockerignore` me `src/` ya `index.html` galti se ignore toh nahi ho gaya.
3. Check karo ki Node version Vite requirements ke compatible hai (`node:20-alpine` supports Vite 5).

### Q39. Port conflict error (`Bind for 0.0.0.0:3000 failed: port is already allocated`) kaise solve karte hain?
**Answer:**
Check karo ki host machine par port 3000 par pehle se koi service chal rahi hai ya nahi (`netstat -ano | findstr :3000` on Windows). Ya toh us process ko kill karo (`taskkill /PID <pid> /F`), ya Compose file me host port change karke `3001:3000` kardo.

### Q40. Buildx kya hai aur simple `docker build` se kaise better hai?
**Answer:** Buildx Docker ka advanced CLI plugin hai jo Moby BuildKit engine use karta hai. Ye parallel layer execution, multi-architecture builds (AMD64 + ARM64/Apple Silicon), secret mounts during build, aur improved cache export support karta hai.

---

## SECTION 10: RAPID FIRE / ONE-LINER VIVA QUESTIONS (Q41 - Q55)

41. **What is an immutable infrastructure?**  
    *Answer:* Servers/containers ko in-place modify nahi karte; koi bhi update naya container build karke deploy karne se hoti hai.
42. **What is Docker's default storage driver on modern Linux/WSL2?**  
    *Answer:* `overlay2` / `overlayfs`.
43. **What is Docker Hub rate limiting?**  
    *Answer:* Anonymous users ke liye 100 pulls per 6 hours limit hoti hai, authenticated users ke liye 200 pulls per 6 hours hoti hai.
44. **What is standard port for PostgreSQL?**  
    *Answer:* Port 5432.
45. **What is standard port for Redis?**  
    *Answer:* Port 6379.
46. **What is standard port for Nginx HTTP?**  
    *Answer:* Port 80.
47. **What is `alpine` Linux and why is it popular in Docker?**  
    *Answer:* Alpine ek ultra-lightweight security-oriented Linux distro hai (~5MB base size), jo images ko lean banata hai.
48. **What does `--runInBand` mean in Jest?**  
    *Answer:* Tests ko sequentially ek hi process me run karta hai (concurrency avoid karta hai), jo database state tests ke liye zaroori hai.
49. **Can a container communicate with another container on different Docker networks?**  
    *Answer:* Nahi, jab tak ki containers same user-defined network se attached na hon ya network bridge connect na ho.
50. **What is a Docker registry vs repository?**  
    *Answer:* Registry ek service hai (jaise Docker Hub) jo multiple repositories store karti hai. Repository ek specific application ki tagged images ka collection hai.
51. **Why do we use `npm install --omit=dev` in backend Dockerfile?**  
    *Answer:* Testing aur dev packages (eslint, nodemon) ko exclude karke production image ko compact aur fast banane ke liye.
52. **How does Nginx handle SPA client-side routing?**  
    *Answer:* `try_files $uri $uri/ /index.html;` directive ke through; agar exact file nahi milti toh fallback index.html ko bhejta hai taaki React router handle kar sake.
53. **What is JWT and where is it stored on frontend?**  
    *Answer:* JSON Web Token stateless auth token hai, TaskFlow me ise browser ke `localStorage` me save kiya gaya hai.
54. **What command is used to inspect container logs in real time?**  
    *Answer:* `docker compose logs -f <service_name>`.
55. **What is the return status code for duplicate registration in TaskFlow?**  
    *Answer:* HTTP 409 Conflict.
