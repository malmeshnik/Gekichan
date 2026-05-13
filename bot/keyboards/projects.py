from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext


def get_projects_keyboard(projects, i18n: I18nContext):
    buttons = []
    for p in projects:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=p["name"], callback_data=f"project_view_{p['id']}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("projects-create"), callback_data="project_create"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_project_detail_keyboard(project_id, i18n: I18nContext):
    buttons = [
        [
            InlineKeyboardButton(
                text="👥 " + i18n.get("projects-add-member"),
                callback_data=f"project_member_add_{project_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text="🗑 " + i18n.get("common-delete"),
                callback_data=f"project_delete_{project_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ " + i18n.get("common-back"), callback_data="projects_list"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_member_add_options_keyboard(project_id, i18n: I18nContext):
    buttons = [
        [
            InlineKeyboardButton(
                text=i18n.get("projects-add-by-username"),
                callback_data=f"project_add_username_{project_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text=i18n.get("projects-add-by-contact"),
                callback_data=f"project_add_contact_{project_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text=i18n.get("common-back"), callback_data=f"project_view_{project_id}"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def project_analytics_keyboard(project_id: int, i18n):

    builder = InlineKeyboardBuilder()

    builder.button(
        text=i18n.buttons.tasks(), callback_data=f"project_tasks_{project_id}"
    )

    builder.button(
        text=i18n.buttons.members(), callback_data=f"project_members_{project_id}"
    )

    builder.button(text=i18n.buttons.back(), callback_data=f"project_view_{project_id}")

    builder.adjust(2, 1)

    return builder.as_markup()
