# Productivity System MVP/V2 Documentation

## Architecture
The system follows a Modular Monolith architecture using Django (DRF) for the backend and Aiogram 3 for the Telegram bot.

### Core Components
- **Backend (DRF)**: Handles business logic, data persistence, and API.
- **Bot (Aiogram)**: Acts as the primary UI/UX layer.
- **Celery**: Manages background tasks, reminders, and timers.
- **PostgreSQL**: Primary database with soft-delete support.
- **Redis**: Broker for Celery and caching.

## Features
- **Multilingual Support**: EN, UK, RU (localized via `aiogram-i18n` and Fluent).
- **Project & Task Management**: CRUD operations with soft-delete.
- **Timer System**: Stopwatch and Focus Countdown (25/50m) modes with Celery-driven notifications.
- **Anti-Procrastination**: Per-user cooldown-based aggressive reminders.
- **Analytics**: Basic productivity scoring and daily reports.

## Localization
Localization is managed via Fluent files in `bot/locales/`. User language is stored in the `User` model.
To add a new language:
1. Create a folder `bot/locales/<lang>/`.
2. Add `messages.ftl`.
3. Update `User.Language` choices in `apps/users/models.py`.

## Services Layer
All business logic is centralized in `apps/<app>/services.py`. Handlers and Views should only call these services.
- `TaskService`
- `ProjectService`
- `FocusSessionService`
- `AntiProcrastinationService`

## Deployment
Use Docker Compose:
```bash
docker-compose up --build
```
Ensure `TELEGRAM_BOT_TOKEN` is set in `.env`.
