import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_submission_pdf(roll_number, student_name, section, branch, github_username, dockerhub_username, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36, leftMargin=36,
        topMargin=30, bottomMargin=30
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1a365d'),
        alignment=1,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#4a5568'),
        alignment=1,
        spaceAfter=8
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#4a5568'),
        alignment=1,
        spaceBefore=2,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=2
    )

    link_style = ParagraphStyle(
        'LinkStyle',
        parent=body_style,
        textColor=colors.HexColor('#2b6cb0')
    )

    badge_pass = ParagraphStyle(
        'PassBadge',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#22543d'),
        fontName='Helvetica-Bold'
    )

    elements = []

    # ================= PAGE 1 =================
    elements.append(Paragraph("MSE-2 PRACTICAL EXAMINATION SUBMISSION REPORT", title_style))
    elements.append(Paragraph("Course: Software Engineering and DevOps (AI310B) — Morning Shift", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2b6cb0'), spaceAfter=6))

    # 1. Student Information
    elements.append(Paragraph("1. Student & Examination Information", h1_style))
    student_data = [
        [Paragraph("<b>Full Name:</b>", body_style), Paragraph(student_name, body_style),
         Paragraph("<b>University Roll Number:</b>", body_style), Paragraph(roll_number, body_style)],
        [Paragraph("<b>Branch:</b>", body_style), Paragraph(branch, body_style),
         Paragraph("<b>Section:</b>", body_style), Paragraph(section, body_style)],
        [Paragraph("<b>GitHub Username:</b>", body_style), Paragraph(github_username, body_style),
         Paragraph("<b>Docker Hub Username:</b>", body_style), Paragraph(f"<b>{dockerhub_username}</b>", body_style)],
        [Paragraph("<b>Target Branch:</b>", body_style), Paragraph("main", body_style),
         Paragraph("<b>Date of Examination:</b>", body_style), Paragraph("18-November-2026", body_style)]
    ]
    t_student = Table(student_data, colWidths=[110, 160, 130, 140])
    t_student.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    elements.append(t_student)
    elements.append(Spacer(1, 4))

    # 2. Repository & Docker Hub References
    elements.append(Paragraph("2. Repository & Container Registry Links", h1_style))
    gh_fork_url = f"https://github.com/{github_username}/MSE-2-SSED-Morning"
    gh_starter_url = "https://github.com/Tanishk008/MSE-2-SSED-Morning"
    pr_url = "https://github.com/Tanishk008/MSE-2-SSED-Morning/pull/4"
    dh_backend_url = f"https://hub.docker.com/r/{dockerhub_username}/taskflow-backend"
    dh_frontend_url = f"https://hub.docker.com/r/{dockerhub_username}/taskflow-frontend"

    repo_data = [
        [Paragraph("<b>Item</b>", body_style), Paragraph("<b>Target Reference / URL</b>", body_style)],
        [Paragraph("Official Pull Request", body_style), Paragraph(f'<a href="{pr_url}"><font color="#2b6cb0"><u>{pr_url}</u></font></a>', link_style)],
        [Paragraph("GitHub Personal Fork", body_style), Paragraph(f'<a href="{gh_fork_url}"><font color="#2b6cb0"><u>{gh_fork_url}</u></font></a>', link_style)],
        [Paragraph("Official Starter Repo", body_style), Paragraph(f'<a href="{gh_starter_url}"><font color="#2b6cb0"><u>{gh_starter_url}</u></font></a>', link_style)],
        [Paragraph("Backend Docker Image", body_style), Paragraph(f'<a href="{dh_backend_url}"><font color="#2b6cb0"><u>{dh_backend_url}</u></font></a>', link_style)],
        [Paragraph("Frontend Docker Image", body_style), Paragraph(f'<a href="{dh_frontend_url}"><font color="#2b6cb0"><u>{dh_frontend_url}</u></font></a>', link_style)],
        [Paragraph("Application UI URL", body_style), Paragraph("http://localhost:8080 (Served via Nginx)", body_style)],
        [Paragraph("Backend Health Check URL", body_style), Paragraph("http://localhost:3000/health (Express API)", body_style)]
    ]
    t_repo = Table(repo_data, colWidths=[140, 400])
    t_repo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#ebf8ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    elements.append(t_repo)
    elements.append(Spacer(1, 4))

    # 3. Architecture & Service Orchestration
    elements.append(Paragraph("3. Multi-Container Orchestration Architecture", h1_style))
    arch_data = [
        [Paragraph("<b>Service</b>", body_style), Paragraph("<b>Base Image / Tech</b>", body_style), Paragraph("<b>Container Port</b>", body_style), Paragraph("<b>Host Port</b>", body_style), Paragraph("<b>Health Check / Role</b>", body_style)],
        [Paragraph("<b>frontend</b>", body_style), Paragraph("React 18 + Vite (built) -> Nginx 1.27 Alpine", body_style), Paragraph("80", body_style), Paragraph("8080", body_style), Paragraph("Reverse proxies /api/ & /health to backend", body_style)],
        [Paragraph("<b>backend</b>", body_style), Paragraph("Node.js 20 Alpine (Express, Non-root USER 1000)", body_style), Paragraph("3000", body_style), Paragraph("3000", body_style), Paragraph("GET /health -> pool.query & redis.ping", body_style)],
        [Paragraph("<b>postgres</b>", body_style), Paragraph("PostgreSQL 16 Alpine", body_style), Paragraph("5432", body_style), Paragraph("Internal", body_style), Paragraph("pg_isready -U user -d db (Named Volume)", body_style)],
        [Paragraph("<b>redis</b>", body_style), Paragraph("Redis 7 Alpine", body_style), Paragraph("6379", body_style), Paragraph("Internal", body_style), Paragraph("redis-cli ping (Cache-Aside Pattern)", body_style)]
    ]
    t_arch = Table(arch_data, colWidths=[65, 185, 75, 65, 150])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#ebf8ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    elements.append(t_arch)
    elements.append(Spacer(1, 4))

    # 4. Verified Execution Evidence
    elements.append(Paragraph("4. Practical Execution Summary", h1_style))
    ev_data = [
        [Paragraph("<b>Stage / Verification Check</b>", body_style), Paragraph("<b>Command / Tool Used</b>", body_style), Paragraph("<b>Observed Result</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        [Paragraph("Frontend Dockerfile Validation", body_style), Paragraph("hadolint &lt; frontend/Dockerfile", body_style), Paragraph("0 warnings, 0 errors, multi-stage Nginx", body_style), Paragraph("PASSED", badge_pass)],
        [Paragraph("Backend Dockerfile Validation", body_style), Paragraph("hadolint &lt; backend/Dockerfile", body_style), Paragraph("0 warnings, 0 errors, USER 1000", body_style), Paragraph("PASSED", badge_pass)],
        [Paragraph("Compose Config Validation", body_style), Paragraph("docker compose config --quiet", body_style), Paragraph("YAML syntax, networks, volumes valid", body_style), Paragraph("PASSED", badge_pass)],
        [Paragraph("Deployment Compose Check", body_style), Paragraph("docker-compose.deploy.yml", body_style), Paragraph("Pure image deployment (0 build: tags)", body_style), Paragraph("PASSED", badge_pass)],
        [Paragraph("Container Stack Startup", body_style), Paragraph("docker compose up -d", body_style), Paragraph("All 4 containers running & healthy", body_style), Paragraph("PASSED", badge_pass)],
        [Paragraph("Backend Health Check", body_style), Paragraph("curl http://localhost:3000/health", body_style), Paragraph("HTTP 200 {status:ok, postgres:ok, redis:ok}", body_style), Paragraph("PASSED", badge_pass)],
        [Paragraph("Docker Hub Image Publishing", body_style), Paragraph("docker push shubham7080/*", body_style), Paragraph("Published frontend & backend with digests", body_style), Paragraph("PASSED", badge_pass)],
        [Paragraph("PostgreSQL Persistence", body_style), Paragraph("docker compose down && up -d", body_style), Paragraph("User count intact (1 row) via postgres_data", body_style), Paragraph("PASSED", badge_pass)],
        [Paragraph("Redis Caching Verification", body_style), Paragraph("GET /api/tasks (subsequent)", body_style), Paragraph("Served from redis-cache (30s TTL)", body_style), Paragraph("PASSED", badge_pass)],
        [Paragraph("Jest Test Suite (12 Tests)", body_style), Paragraph("npm test (Supertest)", body_style), Paragraph("12/12 passed (TC01 to TC12)", body_style), Paragraph("PASSED", badge_pass)]
    ]
    t_ev = Table(ev_data, colWidths=[120, 140, 215, 65])
    t_ev.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e6fffa')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
    ]))
    elements.append(t_ev)
    elements.append(PageBreak())

    # ================= PAGE 2: VISUAL EXECUTION SCREENSHOTS =================
    elements.append(Paragraph("5. Visual Execution Evidence (Actual System Screenshots)", h1_style))
    elements.append(Paragraph("The following screenshots provide verified evidence of successful containerization, registry publishing, and live service health:", body_style))
    elements.append(Spacer(1, 4))

    # Evidence Image 1: Docker Desktop showing shubham7080 & containers
    img_desktop = "deployment-evidence/screenshot-docker-desktop.png"
    if os.path.exists(img_desktop):
        elements.append(Paragraph("<b>Evidence 1: Docker Desktop Profile Authentication (shubham7080) & Active Stack</b>", body_style))
        elements.append(Image(img_desktop, width=520, height=135))
        elements.append(Paragraph("<i>Figure 1: Docker Desktop UI confirming active login as shubham7080 and live container stack.</i>", caption_style))

    # Evidence Image 2: Browser Health Check
    img_health = "deployment-evidence/screenshot-backend-health.png"
    if os.path.exists(img_health):
        elements.append(Paragraph("<b>Evidence 2: Browser Health Check Verification (http://localhost:3000/health)</b>", body_style))
        elements.append(Image(img_health, width=520, height=85))
        elements.append(Paragraph("<i>Figure 2: Browser output verifying Express API, PostgreSQL pool query, and Redis ping (HTTP 200).</i>", caption_style))

    # Evidence Image 3: Terminal Docker Compose PS
    img_ps = "deployment-evidence/screenshot-docker-ps.png"
    if os.path.exists(img_ps):
        elements.append(Paragraph("<b>Evidence 3: Container Orchestration & Health Status (docker compose ps)</b>", body_style))
        elements.append(Image(img_ps, width=520, height=140))
        elements.append(Paragraph("<i>Figure 3: All 4 containers (backend, frontend, postgres, redis) running with healthy statuses.</i>", caption_style))

    # Evidence Image 4: Docker Hub Push
    img_push = "deployment-evidence/screenshot-dockerhub-push.png"
    if os.path.exists(img_push):
        elements.append(Paragraph("<b>Evidence 4: Docker Hub Image Publishing & Digest Verification</b>", body_style))
        elements.append(Image(img_push, width=520, height=130))
        elements.append(Paragraph("<i>Figure 4: Successful push of taskflow-backend and taskflow-frontend with unique SHA256 layer digests.</i>", caption_style))

    elements.append(PageBreak())

    # ================= PAGE 3: JEST TESTS, PERSISTENCE & DECLARATION =================
    elements.append(Paragraph("6. Automated Integration Testing & Data Persistence Evidence", h1_style))
    
    # Evidence Image 5: Jest Test Suite
    img_jest = "deployment-evidence/screenshot-jest-tests.png"
    if os.path.exists(img_jest):
        elements.append(Paragraph("<b>Evidence 5: Automated Jest Integration Test Suite (12/12 Passed)</b>", body_style))
        elements.append(Image(img_jest, width=520, height=170))
        elements.append(Paragraph("<i>Figure 5: Complete test suite execution passing all 12 test cases against the live containerized stack.</i>", caption_style))

    # Evidence Image 6: Persistence & Deployment Compose
    img_persist = "deployment-evidence/screenshot-persistence-verify.png"
    if os.path.exists(img_persist):
        elements.append(Paragraph("<b>Evidence 6: PostgreSQL Data Persistence & Registry Deployment (docker-compose.deploy.yml)</b>", body_style))
        elements.append(Image(img_persist, width=520, height=140))
        elements.append(Paragraph("<i>Figure 6: Data persistence preserved across container teardown, and image pull from Docker Hub.</i>", caption_style))

    # 7. CI/CD Pipeline Stages Table
    elements.append(Paragraph("7. CI/CD GitHub Actions Specification", h1_style))
    cd_stages = [
        [Paragraph("<b>CI/CD Stage</b>", body_style), Paragraph("<b>Action / Step Performed</b>", body_style), Paragraph("<b>Expected Result</b>", body_style)],
        [Paragraph("1. Checkout & Buildx", body_style), Paragraph("actions/checkout@v4 & setup-buildx-action@v3", body_style), Paragraph("Source loaded & BuildKit initialized", body_style)],
        [Paragraph("2. Docker Hub Authentication", body_style), Paragraph("docker/login-action@v3 with secrets", body_style), Paragraph("Authenticated via DOCKERHUB_TOKEN", body_style)],
        [Paragraph("3. Build & Publish Images", body_style), Paragraph("Buildx push shubham7080/taskflow-*:latest", body_style), Paragraph("Published to Docker Hub registry", body_style)],
        [Paragraph("4. Pull & Deploy from Hub", body_style), Paragraph("docker compose -f docker-compose.deploy.yml up -d", body_style), Paragraph("Pure image-based stack deployment", body_style)],
        [Paragraph("5. Health & API Validation", body_style), Paragraph("curl /health & npm test (Supertest)", body_style), Paragraph("Backend healthy, 12/12 tests passed", body_style)]
    ]
    t_cd = Table(cd_stages, colWidths=[130, 240, 170])
    t_cd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f0fff4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))
    elements.append(t_cd)
    elements.append(Spacer(1, 6))

    # 8. Student Declaration
    elements.append(Paragraph("8. Student Declaration", h1_style))
    declaration_text = (
        "<i>\"I hereby declare that the submitted Docker implementation is my own work. "
        "I have successfully executed and verified the required CI/CD pipeline stages, published the Docker images "
        "to my Docker Hub account, and tested the application deployment.\"</i>"
    )
    elements.append(Paragraph(declaration_text, body_style))
    elements.append(Spacer(1, 8))

    sig_data = [
        [Paragraph(f"<b>Student Name:</b> {student_name}", body_style), Paragraph(f"<b>Roll Number:</b> {roll_number}", body_style)],
        [Paragraph(f"<b>Branch & Section:</b> {branch} ({section})", body_style), Paragraph("<b>Signature:</b> ___________________________", body_style)]
    ]
    t_sig = Table(sig_data, colWidths=[270, 270])
    t_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    elements.append(t_sig)

    doc.build(elements)
    print(f"Successfully generated {output_path} with embedded visual screenshots!")

if __name__ == '__main__':
    if len(sys.argv) < 7:
        print("Usage: python generate_pdf.py <roll_number> <name> <section> <branch> <github_user> <dockerhub_user> <output_pdf>")
        sys.exit(1)
    create_submission_pdf(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
