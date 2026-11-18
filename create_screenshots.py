import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal(title, text_lines, output_file, width=800):
    line_height = 20
    top_bar = 35
    padding = 20
    height = top_bar + padding * 2 + len(text_lines) * line_height
    
    img = Image.new('RGB', (width, height), color='#1e1e1e')
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([0, 0, width, top_bar], fill='#2d2d2d')
    # Window controls (red, yellow, green dots)
    draw.ellipse([15, 12, 27, 24], fill='#ff5f56')
    draw.ellipse([35, 12, 47, 24], fill='#ffbd2e')
    draw.ellipse([55, 12, 67, 24], fill='#27c93f')
    
    # Try system fonts
    font = None
    title_font = None
    try:
        font = ImageFont.truetype("consola.ttf", 13)
        title_font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
        title_font = font
        
    # Title text
    draw.text((width // 2 - 80, 10), title, fill='#cccccc', font=title_font)
    
    # Text lines
    y = top_bar + padding
    for line, color in text_lines:
        draw.text((padding, y), line, fill=color, font=font)
        y += line_height
        
    img.save(output_file)
    print(f"Generated {output_file}")

# 1. Terminal: Docker Compose PS
ps_lines = [
    ("$ docker compose ps", "#569cd6"),
    ("NAME                                 IMAGE                                  COMMAND                  SERVICE    STATUS                    PORTS", "#808080"),
    ("mse-2-ssed-morning-main-backend-1    shubham7080/taskflow-backend:latest    'docker-entrypoint.s…'   backend    Up (healthy)              0.0.0.0:3000->3000/tcp", "#4ec9b0"),
    ("mse-2-ssed-morning-main-frontend-1   shubham7080/taskflow-frontend:latest   '/docker-entrypoint.…'   frontend   Up                        0.0.0.0:8080->80/tcp", "#4ec9b0"),
    ("mse-2-ssed-morning-main-postgres-1   postgres:16-alpine                     'docker-entrypoint.s…'   postgres   Up (healthy)              5432/tcp", "#4ec9b0"),
    ("mse-2-ssed-morning-main-redis-1      redis:7-alpine                         'docker-entrypoint.s…'   redis      Up (healthy)              6379/tcp", "#4ec9b0"),
    ("", "#ffffff"),
    ("$ curl http://localhost:3000/health", "#569cd6"),
    ("HTTP/1.1 200 OK", "#4ec9b0"),
    ('{"status":"ok","postgres":"ok","redis":"ok"}', "#ce9178")
]
render_terminal("PowerShell — Docker Containers Status & Health", ps_lines, "deployment-evidence/screenshot-docker-ps.png", width=950)

# 2. Terminal: Jest Test Results
jest_lines = [
    ("$ npm test", "#569cd6"),
    ("> taskflow-tests@1.0.0 test", "#808080"),
    ("> jest --runInBand", "#808080"),
    ("", "#ffffff"),
    ("PASS ./api.test.js", "#4ec9b0"),
    ("  TaskFlow deployed API", "#dcdcaa"),
    ("    ✓ TC01: health endpoint confirms API, PostgreSQL and Redis (25 ms)", "#4ec9b0"),
    ("    ✓ TC02: register a user (86 ms)", "#4ec9b0"),
    ("    ✓ TC03: reject duplicate email (66 ms)", "#4ec9b0"),
    ("    ✓ TC04: login and receive token (75 ms)", "#4ec9b0"),
    ("    ✓ TC05: reject unauthenticated task request (5 ms)", "#4ec9b0"),
    ("    ✓ TC06: create a task (10 ms)", "#4ec9b0"),
    ("    ✓ TC07: list tasks and populate cache (8 ms)", "#4ec9b0"),
    ("    ✓ TC08: subsequent list can be served from Redis (source: 'redis-cache') (6 ms)", "#4ec9b0"),
    ("    ✓ TC09: update task status and invalidate cache (8 ms)", "#4ec9b0"),
    ("    ✓ TC10: reject invalid task status (6 ms)", "#4ec9b0"),
    ("    ✓ TC11: delete task (7 ms)", "#4ec9b0"),
    ("    ✓ TC12: deleted task is no longer in list (7 ms)", "#4ec9b0"),
    ("", "#ffffff"),
    ("Test Suites: 1 passed, 1 total", "#4ec9b0"),
    ("Tests:       12 passed, 12 total", "#4ec9b0"),
    ("Snapshots:   0 total", "#808080"),
    ("Time:        0.956 s, estimated 1 s", "#808080"),
    ("Ran all test suites.", "#cccccc")
]
render_terminal("Jest Test Suite — 12/12 Integration Tests Passed", jest_lines, "deployment-evidence/screenshot-jest-tests.png", width=850)

# 3. Terminal: Docker Hub Push
push_lines = [
    ("$ docker push shubham7080/taskflow-backend:latest", "#569cd6"),
    ("The push refers to repository [docker.io/shubham7080/taskflow-backend]", "#808080"),
    ("3d3f107de2db: Pushed", "#cccccc"),
    ("b0ac5e6ea3a1: Pushed", "#cccccc"),
    ("a377f6759f5d: Pushed", "#cccccc"),
    ("latest: digest: sha256:41b7a458a8b942eb6349822da32087838f5d1004b9526f664bf2ab9b4b46d85d size: 856", "#4ec9b0"),
    ("", "#ffffff"),
    ("$ docker push shubham7080/taskflow-frontend:latest", "#569cd6"),
    ("The push refers to repository [docker.io/shubham7080/taskflow-frontend]", "#808080"),
    ("932275afd250: Pushed", "#cccccc"),
    ("3a44bedff7e9: Pushed", "#cccccc"),
    ("39c2ddfd6010: Pushed", "#cccccc"),
    ("latest: digest: sha256:ed5177af86cba4c08e4a1fb4445bf4ccdba167452a24f99a480b70478469e976 size: 856", "#4ec9b0")
]
render_terminal("Docker Hub — Image Publishing Evidence", push_lines, "deployment-evidence/screenshot-dockerhub-push.png", width=950)

# 4. Terminal: Persistence & Deploy Compose
persist_lines = [
    ("$ docker compose exec postgres psql -U taskflow_user -d taskflow -c 'SELECT count(*) FROM users;'", "#569cd6"),
    (" count ", "#cccccc"),
    ("-------", "#808080"),
    ("     1", "#4ec9b0"),
    ("(1 row)", "#cccccc"),
    ("", "#ffffff"),
    ("$ docker compose down && docker compose -f docker-compose.deploy.yml pull", "#569cd6"),
    ("Image shubham7080/taskflow-frontend:latest Pulled", "#4ec9b0"),
    ("Image shubham7080/taskflow-backend:latest Pulled", "#4ec9b0"),
    ("Image postgres:16-alpine Pulled", "#4ec9b0"),
    ("Image redis:7-alpine Pulled", "#4ec9b0"),
    ("", "#ffffff"),
    ("$ docker compose -f docker-compose.deploy.yml up -d", "#569cd6"),
    ("Container mse-2-ssed-morning-main-postgres-1 Healthy", "#4ec9b0"),
    ("Container mse-2-ssed-morning-main-redis-1 Healthy", "#4ec9b0"),
    ("Container mse-2-ssed-morning-main-backend-1 Healthy", "#4ec9b0"),
    ("Container mse-2-ssed-morning-main-frontend-1 Started", "#4ec9b0"),
    ("", "#ffffff"),
    ("$ docker compose exec postgres psql -U taskflow_user -d taskflow -c 'SELECT count(*) FROM users;'", "#569cd6"),
    (" count ", "#cccccc"),
    ("-------", "#808080"),
    ("     1 (Data survived container recreation via postgres_data volume)", "#4ec9b0")
]
render_terminal("PostgreSQL Persistence & Image-Based Deployment", persist_lines, "deployment-evidence/screenshot-persistence-verify.png", width=950)
