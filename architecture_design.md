# Productivity System Architecture Design

## 1. System Architecture Overview

The system follows a **Modular Monolith** architecture pattern. This approach ensures ease of deployment and development for the MVP phase while allowing for a clear separation of concerns that facilitates future migration to microservices if needed.

### Components:
- **Django REST Framework (DRF) Backend**: The core of the system, handling business logic, data persistence, and API provisioning.
- **Aiogram 3 Telegram Bot**: Acts as a lightweight interface for quick actions (task creation, status updates) and proactive notifications (reminders, reports).
- **React Mini App**: The rich user interface for project management, focus timers, and detailed analytics.
- **PostgreSQL**: Primary relational database.
- **Redis**: Used for caching and as a message broker for Celery.
- **Celery**: Handles background tasks, scheduled reports, and asynchronous notifications.

### Communication Flow:
- **Bot <-> Backend**: The Bot interacts with the Backend via internal service calls (if running in same process) or REST API using a secure Internal-Service-Token.
- **Mini App <-> Backend**: The Mini App communicates via a REST API using JWT for authentication.
- **Real-time**: Not required for MVP; the Mini App uses standard HTTP requests, and the Bot uses Webhooks or Long Polling to receive updates from Telegram.

---

## 2. Services Breakdown

### Auth / Users Service
- **Responsibilities**: Telegram `initData` verification, user registration, JWT generation, session management.
- **Logic**: Verifies the HMAC-SHA256 signature of Telegram data to ensure authenticity.

### Projects Service
- **Responsibilities**: Project lifecycle (create/update/delete), member management (adding/removing users), and role assignments (owner/member).

### Tasks Service
- **Responsibilities**: Task CRUD operations, status transitions (Todo -> In Progress -> Done), assignment of users to tasks, and deadline tracking.

### Focus Sessions Service
- **Responsibilities**: Managing session logs (start, stop, pause timestamps), calculating net duration, and linking sessions to tasks.

### Analytics Service
- **Responsibilities**: Aggregating raw data into `DailyStats`, calculating productivity scores, and generating historical trends (7d/30d).

### Notifications Service
- **Responsibilities**: Scheduling and dispatching reminders, daily/morning reports via the Telegram Bot Handler.

---

## 3. Database Schema (PostgreSQL)

### Tables & Fields

#### `users`
- `id`: BigInt (Telegram ID as PK)
- `username`: String (nullable)
- `first_name`: String
- `last_name`: String (nullable)
- `timezone`: String (default: 'UTC')
- `created_at`: DateTime

#### `projects`
- `id`: UUID
- `name`: String
- `description`: Text (nullable)
- `owner_id`: FK(users.id)
- `created_at`: DateTime

#### `project_members`
- `project_id`: FK(projects.id)
- `user_id`: FK(users.id)
- `role`: Enum ('owner', 'member')
- **Unique**: (`project_id`, `user_id`)

#### `tasks`
- `id`: UUID
- `project_id`: FK(projects.id)
- `creator_id`: FK(users.id)
- `assignee_id`: FK(users.id, nullable)
- `title`: String
- `description`: Text (nullable)
- `status`: Enum ('todo', 'in_progress', 'done')
- `deadline`: DateTime (nullable)
- `created_at`: DateTime

#### `focus_sessions`
- `id`: UUID
- `user_id`: FK(users.id)
- `task_id`: FK(tasks.id, nullable)
- `start_time`: DateTime
- `end_time`: DateTime (nullable)
- `duration`: Integer (net focus time in seconds)
- `interruptions_count`: Integer (default: 0)
- `context`: String (e.g., 'work', 'study')

#### `daily_stats`
- `id`: UUID
- `user_id`: FK(users.id)
- `date`: Date
- `total_focus_time`: Integer (seconds)
- `completed_tasks_count`: Integer
- `interruptions_count`: Integer
- `productivity_score`: Decimal
- **Unique**: (`user_id`, `date`)

### Performance & Scalability Considerations
- **Indexes**:
  - `tasks(project_id, status)`: For fast retrieval of board views.
  - `focus_sessions(user_id, start_time)`: For analytics calculations.
  - `daily_stats(user_id, date)`: For dashboard loading.
- **Partitioning**: For `focus_sessions` and `daily_stats` by date if the data grows significantly (beyond MVP).
- **BigInt for IDs**: Use Telegram IDs as primary keys where applicable to avoid unnecessary mapping tables.

---

## 4. API Design (DRF)

### Authentication
- **Method**: JWT (JSON Web Token)
- **Flow**:
  1. Frontend (Mini App) sends `initData` from Telegram to `/api/auth/telegram/`.
  2. Backend validates `initData` hash.
  3. Backend retrieves or creates User.
  4. Backend returns `access` and `refresh` tokens.

### Endpoints

#### Projects
- `GET /api/projects/` - List user's projects.
- `POST /api/projects/` - Create a new project.
- `GET /api/projects/{id}/` - Project details & member list.
- `PATCH /api/projects/{id}/` - Update project.

#### Tasks
- `GET /api/tasks/?project_id={id}&status={status}` - Filtered task list.
- `POST /api/tasks/` - Create task.
- `PATCH /api/tasks/{id}/` - Update status/assignee/details.

#### Focus Sessions
- `POST /api/sessions/start/` - Log start of a session (returns session ID).
- `PATCH /api/sessions/{id}/stop/` - Log completion and final duration.
- `GET /api/sessions/` - Recent session history.

#### Stats & Analytics
- `GET /api/stats/today/` - Summary for current day.
- `GET /api/stats/dashboard/` - Data for 7d/30d charts.
- `GET /api/stats/recommendations/` - Daily rule-based suggestions.

### Pagination & Filtering
- Use `django-filter` for status and date range filtering.
- Standard limit/offset pagination for task and session history.

---

## 5. Telegram Bot Architecture (Aiogram 3)

### Structure
- `bot.py`: Entry point (dispatcher initialization).
- `handlers/`:
  - `common.py`: `/start`, `/help`, and basic commands.
  - `projects.py`: Project management via inline buttons.
  - `tasks.py`: Task CRUD and status updates.
  - `messages.py`: "Create task from message" logic.
- `keyboards/`: Inline and reply keyboard builders.
- `middlewares/`:
  - `auth.py`: Injects user context from backend for each request.
- `services/`: API client for communicating with the DRF backend.

### Key Workflows
- **Create Task from Message**:
  - User forwards or sends a message.
  - Bot provides an inline button "➕ Add as Task".
  - Upon click, bot prompts for project selection via inline menu.
- **Reminders**:
  - Celery worker triggers a bot method to send proactive messages to specific `user_id`s.

---

## 6. React Mini App Architecture

### Technical Stack
- **Framework**: React + Vite
- **State Management**: **Zustand** (lightweight, easy to use with hooks).
- **Styling**: Tailwind CSS + Telegram WebApp CSS variables (for native look).
- **API Client**: Axios with interceptors for JWT injection and 401 handling.

### Page Structure
- **Dashboard**: Quick stats (today's focus time, tasks done), active project list.
- **Task Board**: Kanban-style or list view of tasks with status filters.
- **Focus Timer**: Prominent countdown/count-up timer with start/pause/stop and task linkage.
- **Stats**: Visualized charts (Recharts) for 7d/30d productivity trends.

### Telegram Integration
- Use `@twa-dev/sdk` for:
  - Theme synchronization.
  - Closing the app or showing alerts.
  - Handling `back_button` and `main_button`.
  - Retrieving `initData` for authentication.

---

## 7. Productivity Insights & Analytics Logic

### Productivity Score Calculation
The system uses a weighted formula to calculate the daily score:
`Score = (CompletedTasks * 1.0) + (FocusHours * 2.0) - (Interruptions * 0.5)`

### Rule-based Recommendations (MVP)
- **Time Peak Insight**: "You are most productive between 10 AM and 1 PM. Schedule your 'Deep Work' sessions then."
- **Consistency Push**: "You've hit your focus goal 3 days in a row! Keep the streak alive."
- **Recovery Suggestion**: "You had 5 interruptions yesterday. Try a shorter Pomodoro interval (20 min) today to build momentum."

### Anti-Procrastination Triggers
- **Idle Alert**: If no tasks moved to `done` and no focus sessions started by 2 PM.
- **Overdue Warning**: Bot notification for tasks past their deadline.

---

## 8. Background Jobs & Scheduling

### Tooling: Celery + Redis + Celery Beat
- **Daily Reports**: Scheduled via Celery Beat to run at the end of the day (relative to user's timezone).
- **Morning Summaries**: Scheduled to run in the morning to provide focus for the day.
- **Anti-Procrastination Triggers**: Periodic checks (every hour) for overdue tasks or zero-focus-time alerts.
- **Stats Aggregation**: Incremental updates to `daily_stats` can be triggered by session completion or task status changes to keep the analytics responsive.

---

## 9. Performance & Scaling

### Caching Strategy (Redis)
- Cache expensive analytics queries for historical stats (7d/30d).
- Cache user session and authentication states.

### DB Indexing
- Targeted indexes on `project_id`, `user_id`, and `status` fields as defined in the DB section.

### Scaling
- **Horizontal**: Backend and Bot services can be scaled horizontally behind a load balancer (e.g., Nginx).
- **Concurrency**: Use Gunicorn with Uvicorn workers for high-concurrency async support in the DRF backend.

---

## 10. Security

- **Authentication**: Telegram `initData` verification is mandatory. Use Short-lived JWTs.
- **Rate Limiting**: Implement DRF's `ScopedRateThrottle` for sensitive endpoints (Auth, Task creation).
- **Data Protection**: Encryption at rest for DB. Use HTTPS for all communications.
- **Internal API**: Bot-to-Backend communication secured via IP whitelisting or pre-shared secret tokens.

---

## 11. Deployment Architecture

### Docker Setup
- `docker-compose.yml` defining services:
  - `backend`: DRF application.
  - `bot`: Aiogram runner.
  - `frontend`: Nginx serving the React build.
  - `celery_worker`: Background job runner.
  - `celery_beat`: Task scheduler.
  - `postgres`: Database.
  - `redis`: Broker and Cache.

### CI/CD
- GitHub Actions for:
  - Running Python and JS linting/tests.
  - Building and pushing Docker images to a registry.
  - Automated deployment to a staging/production server via SSH.

---
