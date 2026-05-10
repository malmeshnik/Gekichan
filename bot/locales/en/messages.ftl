# Common
common-back = ⬅️ Back
common-cancel = ❌ Cancel
common-delete = 🗑 Delete
common-confirm-delete = ⚠️ Delete?
common-search = 🔍 Search
common-settings = ⚙️ Settings
common-save = 💾 Save
common-edit = ✏️ Edit
common-active-now = 🟢 Active now
common-last-active = Last active: { $time } ago

# Navigation
nav-home = 🏠 Home
nav-projects = 📁 Projects
nav-tasks = 📝 Tasks
nav-focus = 🔥 Focus
nav-stats = 📊 Stats

# Projects
projects-title = 📁 Your Projects
projects-empty = You don't have any projects yet.
projects-create = ➕ Create Project
projects-search = 🔍 Search
projects-archive = 📂 Archive
projects-summary = 👥 { $members }  📝 { $tasks } { $overdue ->
    [0] {""}
    *[other]   ⚠️ { $overdue } overdue
}

# Project Dashboard
project-dashboard-members = 👥 Members: { $total }
project-dashboard-active = 🟢 Active now: { $active }
project-dashboard-tasks = 📝 Tasks: { $total }
project-dashboard-in-progress = 🔥 In Progress: { $count }
project-dashboard-overdue = ⚠️ Overdue: { $count }
project-dashboard-done = ✅ Done: { $count }
project-dashboard-focus = ⏱ Focus tracked: { $time }
project-dashboard-activity = Last activity: { $time } ago

project-btn-tasks = 📝 Tasks
project-btn-new-task = ➕ New
project-btn-members = 👥 Members
project-btn-analytics = 📊 Analytics
project-btn-focus = 🔥 Focus
project-btn-settings = ⚙️ Settings

# Tasks
tasks-grouped-in-progress = 🔥 In Progress
tasks-grouped-overdue = ⚠️ Overdue
tasks-grouped-todo = 📌 Todo
tasks-grouped-done = ✅ Done

task-card-assignee = 👤 { $name }
task-card-deadline = 📅 { $date }
task-card-priority = { $priority ->
    [high] 🔴 High
    [medium] 🟡 Medium
    *[low] 🟢 Low
}
task-card-focus = ⏱ { $time }
task-card-attachments = 📎 { $count }

# Task Details
task-details-status = Status: { $status }
task-details-priority = Priority: { $priority }
task-details-activity = Last activity: { $time }

task-btn-start-focus = ▶️ Start Focus
task-btn-stop-focus = ⏹ Stop Focus
task-btn-complete = ✅ Complete
task-btn-reassign = 👤 Reassign
task-btn-attachments = 📎 Attachments

# Members
members-title = 👥 Members
members-role-owner = Owner
members-role-member = Member
members-btn-add = ➕ Add Member
members-btn-manage-roles = ✏️ Manage Roles

# Search
search-prompt = 🔍 Enter search query:
search-no-results = No results found for "{ $query }"

# Confirmations
confirm-delete-project = ⚠️ Delete project?
confirm-delete-project-note = { $count } tasks will be archived.
confirm-remove-member = Remove { $name } from project?
