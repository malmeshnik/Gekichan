# Common
common-back = ⬅️ Назад
common-cancel = ❌ Отмена
common-delete = 🗑 Удалить
common-confirm-delete = ⚠️ Удалить?
common-search = 🔍 Поиск
common-settings = ⚙️ Настройки
common-save = 💾 Сохранить
common-edit = ✏️ Редактировать
common-active-now = 🟢 Активен сейчас
common-last-active = Активность: { $time } назад

# Navigation
nav-home = 🏠 Главная
nav-projects = 📁 Проекты
nav-tasks = 📝 Задачи
nav-focus = 🔥 Фокус
nav-stats = 📊 Статистика

# Projects
projects-title = 📁 Ваши Проекты
projects-empty = У вас еще нет проектов.
projects-create = ➕ Создать проект
projects-search = 🔍 Поиск
projects-archive = 📂 Архив
projects-summary = 👥 { $members }  📝 { $tasks } { $overdue ->
    [0] {""}
    *[other]   ⚠️ { $overdue } просрочено
}

# Project Dashboard
project-dashboard-members = 👥 Участники: { $total }
project-dashboard-active = 🟢 Активны: { $active }
project-dashboard-tasks = 📝 Задачи: { $total }
project-dashboard-in-progress = 🔥 В работе: { $count }
project-dashboard-overdue = ⚠️ Просрочено: { $count }
project-dashboard-done = ✅ Выполнено: { $count }
project-dashboard-focus = ⏱ Отслежено: { $time }
project-dashboard-activity = Последняя активность: { $time } назад

project-btn-tasks = 📝 Задачи
project-btn-new-task = ➕ Новая
project-btn-members = 👥 Участники
project-btn-analytics = 📊 Аналитика
project-btn-focus = 🔥 Фокус
project-btn-settings = ⚙️ Настр.

# Tasks
tasks-grouped-in-progress = 🔥 В работе
tasks-grouped-overdue = ⚠️ Просрочено
tasks-grouped-todo = 📌 Нужно сделать
tasks-grouped-done = ✅ Выполнено

task-card-assignee = 👤 { $name }
task-card-deadline = 📅 { $date }
task-card-priority = { $priority ->
    [high] 🔴 Высокий
    [medium] 🟡 Средний
    *[low] 🟢 Низкий
}
task-card-focus = ⏱ { $time }
task-card-attachments = 📎 { $count }

# Task Details
task-details-status = Статус: { $status }
task-details-priority = Приоритет: { $priority }
task-details-activity = Последняя активность: { $time }

task-btn-start-focus = ▶️ Начать фокус
task-btn-stop-focus = ⏹ Остановить
task-btn-complete = ✅ Выполнено
task-btn-reassign = 👤 Назначить
task-btn-attachments = 📎 Вложения

# Members
members-title = 👥 Участники
members-role-owner = Владелец
members-role-member = Участник
members-btn-add = ➕ Добавить
members-btn-manage-roles = ✏️ Роли

# Search
search-prompt = 🔍 Введите запрос для поиска:
search-no-results = Ничего не найдено по запросу "{ $query }"

# Confirmations
confirm-delete-project = ⚠️ Удалить проект?
confirm-delete-project-note = { $count } задач будет архивировано.
confirm-remove-member = Удалить { $name } из проекта?
