# Common
common-back = ⬅️ Назад
common-cancel = ❌ Скасувати
common-delete = 🗑 Видалити
common-confirm-delete = ⚠️ Видалити?
common-search = 🔍 Пошук
common-settings = ⚙️ Налаштування
common-save = 💾 Зберегти
common-edit = ✏️ Редагувати
common-active-now = 🟢 Активний зараз
common-last-active = Активність: { $time } тому

# Navigation
nav-home = 🏠 Головна
nav-projects = 📁 Проєкти
nav-tasks = 📝 Завдання
nav-focus = 🔥 Фокус
nav-stats = 📊 Статистика

# Projects
projects-title = 📁 Ваші Проєкти
projects-empty = У вас ще немає проєктів.
projects-create = ➕ Створити проєкт
projects-search = 🔍 Пошук
projects-archive = 📂 Архів
projects-summary = 👥 { $members }  📝 { $tasks } { $overdue ->
    [0] {""}
    *[other]   ⚠️ { $overdue } прострочено
}

# Project Dashboard
project-dashboard-members = 👥 Учасники: { $total }
project-dashboard-active = 🟢 Активні: { $active }
project-dashboard-tasks = 📝 Завдання: { $total }
project-dashboard-in-progress = 🔥 В роботі: { $count }
project-dashboard-overdue = ⚠️ Прострочено: { $count }
project-dashboard-done = ✅ Виконано: { $count }
project-dashboard-focus = ⏱ Відстежено: { $time }
project-dashboard-activity = Остання активність: { $time } тому

project-btn-tasks = 📝 Завдання
project-btn-new-task = ➕ Нове
project-btn-members = 👥 Учасники
project-btn-analytics = 📊 Аналітика
project-btn-focus = 🔥 Фокус
project-btn-settings = ⚙️ Налашт.

# Tasks
tasks-grouped-in-progress = 🔥 В роботі
tasks-grouped-overdue = ⚠️ Прострочено
tasks-grouped-todo = 📌 Треба зробити
tasks-grouped-done = ✅ Виконано

task-card-assignee = 👤 { $name }
task-card-deadline = 📅 { $date }
task-card-priority = { $priority ->
    [high] 🔴 Високий
    [medium] 🟡 Середній
    *[low] 🟢 Низький
}
task-card-focus = ⏱ { $time }
task-card-attachments = 📎 { $count }

# Task Details
task-details-status = Статус: { $status }
task-details-priority = Пріоритет: { $priority }
task-details-activity = Остання активність: { $time }

task-btn-start-focus = ▶️ Почати фокус
task-btn-stop-focus = ⏹ Зупинити
task-btn-complete = ✅ Виконано
task-btn-reassign = 👤 Призначити
task-btn-attachments = 📎 Вкладення

# Members
members-title = 👥 Учасники
members-role-owner = Власник
members-role-member = Учасник
members-btn-add = ➕ Додати
members-btn-manage-roles = ✏️ Ролі

# Search
search-prompt = 🔍 Введіть запит для пошуку:
search-no-results = Нічого не знайдено за запитом "{ $query }"

# Confirmations
confirm-delete-project = ⚠️ Видалити проєкт?
confirm-delete-project-note = { $count } завдань буде архівовано.
confirm-remove-member = Видалити { $name } з проєкту?
