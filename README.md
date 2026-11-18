# 🚀 FastAPI Backend Engineering Suite & Ethical Ingestion Pipeline

A modular, production-ready backend suite built with **Python 3.10+**, **FastAPI**, **PostgreSQL**, **SQLite**, and **Supabase Auth**, paired with an ethical, schema-validated web scraping engine. Engineered by **Anurag Yadav** for the **FlyRank.ai AI Backend Engineering Track**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Auth%20%26%20JWT-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Docker](https://img.shields.io/badge/Docker-PostgreSQL%20Stack-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![SQLite](https://img.shields.io/badge/SQLite-ACID%20Persistence-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-8%2F8%20Passing-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)

---

## 📌 Executive Summary & Milestones

This repository traces the practical evolution of backend engineering from basic in-memory operations to containerized microservices, cryptographic identity verification, and automated data ingestion:

| Milestone | Architecture | Storage / Engine | Entrypoint | Verified Status |
| :--- | :--- | :--- | :--- | :---: |
| **Task 1** | Ephemeral In-Memory REST API | Volatile Python data store | `backend/task1_main.py` | ✅ Verified |
| **Task 2** | Embedded ACID SQL Persistence | SQLite (`database/tasks.db`) | `backend/task2_main.py` | ✅ Verified |
| **Task 3** | Containerized Multi-Tier Service | PostgreSQL 16 + Docker Compose | `backend/task3_main.py` | ✅ Verified |
| **Task 4** | Identity Provider & Guarded Routes | Supabase Auth + JWT Verification | `backend/main.py` | ✅ Verified |
| **Task 5 (A9)** | Ethical Web Ingestion Pipeline | BeautifulSoup4 + Pydantic Schema | `scraper/src/main.py` | ✅ Verified |

---

## 📂 Repository Structure

```
CRUD-API/
├── backend/
│   ├── task1_main.py       # Task 1: In-memory REST API with input validation
│   ├── task2_main.py       # Task 2: SQLite database API with filtering, search & sorting
│   ├── task3_main.py       # Task 3: PostgreSQL Docker service with connection pooling
│   └── main.py             # Task 4: Supabase Auth, JWT verification & route guards
├── scraper/
│   ├── src/
│   │   ├── config.py       # Politeness rules (User-Agent, rate limiting, timeouts)
│   │   ├── client.py       # Polite HTTP client with 2-tier disk caching
│   │   ├── crawler.py      # Catalogue traversal (3 pages, 60 book URLs)
│   │   ├── extractor.py    # BeautifulSoup product DOM parsing
│   │   ├── normalizer.py   # Type cleaning & URL resolution
│   │   ├── schemas.py      # Pydantic validation models
│   │   ├── reporter.py     # Execution metrics & JSON reporting
│   │   └── main.py         # Complete scraper CLI entrypoint
│   ├── tests/              # Scraper unit test suite & offline HTML fixtures
│   ├── output/             # books.json (60 records) and run-report.json
│   └── README.md           # Scraper documentation & target classification
├── Docs/                   # Verification screenshots & official project briefs
│   ├── task1_root_success.png
│   ├── task2_root_success.png
│   ├── task4_supabase_connected.png
│   ├── Swagger_Auth.png
│   ├── postgres_table.png
│   └── sql_select_all.png
├── tests/
│   └── test_api.py         # Shared API contract regression test suite
├── compose.yaml            # Docker Compose multi-service definition (api + db)
├── dockerfile              # Multi-stage production container build
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Universal Python requirements
├── .env.example            # Environment variables template
└── LICENSE                 # Proprietary License (Copyright © 2026 Anurag Yadav)
```

---

## ⚡ Quickstart & Installation

### 1. Environment Setup
```bash
git clone https://github.com/imanurag2311/CRUD-API.git
cd CRUD-API

# Install required dependencies:
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the template and supply your credentials:
```bash
cp .env.example .env
```

Your `.env` contains:
```ini
# PostgreSQL (Task 3):
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=tasks
DATABASE_URL=postgres://postgres:your_secure_password@localhost:5432/tasks

# Supabase Auth (Task 4):
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_anon_public_key
PORT=8000
```

---

## 🖥️ Milestone Execution & Terminal Verification

### 🔹 Task 1: In-Memory CRUD API
```bash
python -m uvicorn backend.task1_main:app --reload --port 8000
```
- **Service Discovery (`GET /`):**
  ```json
  {"name": "Task API", "version": "1.0", "endpoints": ["/tasks", "/health"]}
  ```
  ![Task 1 Root](Docs/task1_root_success.png)
- **Terminal Verification (`curl -i`):**
  ```bash
  curl -i http://localhost:8000/health
  # HTTP/1.1 200 OK -> {"status":"ok"}

  curl -i -X POST http://localhost:8000/tasks \
    -H "Content-Type: application/json" \
    -d '{"title": "Complete Task 1"}'
  # HTTP/1.1 201 Created -> {"id":3,"title":"Complete Task 1","done":false}
  ```
- **The Persistence Observation:** Data lives exclusively in memory variables (`tasks = [...]`). When the process terminates, all mutations vanish and revert to seed defaults—proving the architectural need for databases.

---

### 🔹 Task 2: SQLite Persistent Database
```bash
python -m uvicorn backend.task2_main:app --reload --port 8000
```
- **Service Discovery (`GET /`):**
  ```json
  {"name": "Task API (Database)", "version": "2.0", "endpoints": ["/tasks", "/stats", "/health"]}
  ```
  ![Task 2 Root](Docs/task2_root_success.png)
- **Persistence Guarantee:** `database/tasks.db` is auto-created and seeded only when empty. Mutations persist permanently across server restarts.
- **Direct SQL Exploration:** Database inspected via DB Browser for SQLite:
  ```sql
  SELECT * FROM tasks WHERE done = 1;
  ```
  ![SQLite Inspection](Docs/sql_select_all.png)

---

### 🔹 Task 3: Containerized PostgreSQL Stack
```bash
docker compose up -d --build
```
- **Orchestration:** Starts both FastAPI (`api`) and PostgreSQL 16 (`db`) within private Docker network `tasknet`.
- **Durability:** Backed by persistent named volume `taskdata`. Running `docker compose down` and `docker compose up` preserves all data.
- **Direct Container SQL Check:**
  ```bash
  docker exec -it crud_api_db psql -U postgres -d tasks -c "\dt"
  ```
  ![PostgreSQL Table](Docs/postgres_table.png)

---

### 🔹 Task 4: Supabase Authentication & Guarded Routes
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
- **Terminal Startup Output:**
  ```text
  INFO:     Started server process [7832]
  INFO:     Waiting for application startup.
  🚀 Server running and connected to Supabase
  INFO:     Application startup complete.
  ```
- **Service Verification (`GET /`):**
  ```json
  {"message": "Server running & connected to Supabase"}
  ```
  ![Task 4 Live Supabase Connection](Docs/task4_supabase_connected.png)
- **Interactive Swagger Authorize Padlock:**
  Open `http://localhost:8000/docs` to authenticate directly with Bearer tokens:
  ![Swagger Auth Padlock](Docs/Swagger_Auth.png)
- **Terminal Auth Flow (`curl -i`):**
  ```bash
  # 1. Sign up:
  curl -i -X POST http://localhost:8000/auth/signup \
    -H "Content-Type: application/json" \
    -d '{"email": "anurag.test@gmail.com", "password": "Password123!"}'
  # HTTP/1.1 201 Created

  # 2. Log in & acquire JWT:
  curl -i -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email": "anurag.test@gmail.com", "password": "Password123!"}'
  # HTTP/1.1 200 OK -> {"access_token": "eyJhbGciOi...", "token_type": "bearer"}

  # 3. Access protected route:
  curl -i http://localhost:8000/protected/profile \
    -H "Authorization: Bearer <TOKEN>"
  # HTTP/1.1 200 OK -> {"id": "...", "email": "anurag.test@gmail.com"}

  # 4. Forged/invalid token rejection:
  curl -i http://localhost:8000/protected/profile \
    -H "Authorization: Bearer forged_token"
  # HTTP/1.1 401 Unauthorized -> {"error": "Invalid or expired token"}
  ```

---

### 🔹 Task 5 (A9): The Polite Web Scraper
```bash
python -m scraper.src.main
```
- **Execution Telemetry Output:**
  ```text
  ======================================================================
  🚀 FLYRANK BACKEND TRACK · ASSIGNMENT A9: THE POLITE SCRAPER
  ======================================================================
  --- STAGE 0: Target Classification & Robots Check ---
  Target: https://books.toscrape.com/ (Designated Practice Sandbox)
  Scope: Exactly 3 catalogue pages (60 books)
  Robots: https://books.toscrape.com/robots.txt -> Checked (no robots file found)

  --- STAGE 1 & 2: Catalogue Crawling & URL Discovery ---
  🔍 Starting catalogue crawl: 3 pages discovered -> 60 unique book URLs

  --- STAGE 3, 4 & 5: Detail Extraction, Normalization & Validation ---
  🧪 [CHAOS TEST] Injected 1 deliberate fake URL: non_existent_book_9999/index.html
  ⚠️ SKIPPED broken page: non_existent_book_9999/index.html (HTTP 404: Not Found)
  ✅ Extraction complete: 60 unique validated books (survived 1 bad page)

  ======================================================================
  🏁 EXECUTION TELEMETRY SUMMARY
  ======================================================================
    • Target:                  https://books.toscrape.com/
    • Duration:                0.23s
    • Catalogue Pages Crawled: 3
    • Detail Pages Fetched:    60
    • Cache Hits:              63
    • Valid Records:           60
    • Invalid Records:         0
    • Failed Pages (Chaos):    1
  ======================================================================
  ```
- **Unit Test Suite (`pytest scraper/tests/ -v`):**
  ```text
  scraper/tests/test_scraper.py::test_price_normalization PASSED           [ 12%]
  scraper/tests/test_scraper.py::test_rating_conversion PASSED             [ 25%]
  scraper/tests/test_scraper.py::test_availability_parsing PASSED          [ 37%]
  scraper/tests/test_scraper.py::test_relative_to_absolute_url PASSED      [ 50%]
  scraper/tests/test_scraper.py::test_missing_description_from_fixture PASSED [ 62%]
  scraper/tests/test_scraper.py::test_malformed_html_fixture PASSED        [ 75%]
  scraper/tests/test_scraper.py::test_valid_book_extraction PASSED         [ 87%]
  scraper/tests/test_scraper.py::test_pydantic_schema_validation PASSED    [100%]
  ============================== 8 passed in 0.63s ==============================
  ```

---

## 📡 Complete API Endpoint Reference

### Authentication & Access Control (`backend/main.py`)
| Method | Endpoint | Status Codes | Description | Auth Required |
| :---: | :--- | :---: | :--- | :---: |
| `GET` | `/` | `200` | Service discovery & Supabase probe | None |
| `GET` | `/health` | `200` | Operational health probe | None |
| `POST` | `/auth/signup` | `201`, `400` | Registers user with email & password | None |
| `POST` | `/auth/login` | `200`, `400`, `401` | Authenticates user; returns JWT session | None |
| `GET` | `/public/info` | `200` | Public unauthenticated data | None |
| `GET` | `/protected/profile` | `200`, `401` | Returns authenticated user profile | **Bearer JWT** |
| `GET` | `/protected/dashboard` | `200`, `401` | Protected user dashboard | **Bearer JWT** |
| `POST` | `/auth/logout` | `204`, `401` | Terminates active user session | **Bearer JWT** |

### Task Management CRUD (`backend/task1_main.py` - `task3_main.py`)
| Method | Endpoint | Status Codes | Description | Request Body |
| :---: | :--- | :---: | :--- | :---: |
| `GET` | `/tasks` | `200` | Retrieve list of all tasks | None |
| `GET` | `/tasks/{id}` | `200`, `404` | Retrieve single task by ID | None |
| `POST` | `/tasks` | `201`, `400` | Create a new task | `{"title": "string"}` |
| `PUT` | `/tasks/{id}` | `200`, `400`, `404` | Update task title and/or done status | `{"title"?: "str", "done"?: bool}` |
| `DELETE` | `/tasks/{id}` | `204`, `404` | Delete task by ID | None |

---

## ⚖️ License & Copyright

**Copyright © 2026 Anurag Yadav. All Rights Reserved.**  
Developed for the FlyRank.ai AI Backend Engineering Internship Track.
