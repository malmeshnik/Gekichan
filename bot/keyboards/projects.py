from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from bot.utils.callbacks import (
    ProjectViewCb,
    ProjectActionCb,
    ProjectListCb,
    ProjectMemberAddCb,
    ProjectTasksCb,
    ProjectMembersCb,
)

def get_projects_keyboard(projects, i18n: I18nContext):
    buttons = []
    for p in projects:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=p["name"], callback_data=ProjectViewCb(id=p["id"]).pack()
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("projects-create"), callback_data=ProjectActionCb(action="create").pack()
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_project_detail_keyboard(project_id, i18n: I18nContext):
    buttons = [
        [
            InlineKeyboardButton(
                text="👥 " + i18n.get("projects-add-member"),
                callback_data=ProjectMemberAddCb(project_id=project_id).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🗑 " + i18n.get("common-delete"),
                callback_data=ProjectActionCb(action="delete_confirm", id=project_id).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ " + i18n.get("common-back"), callback_data=ProjectListCb(page=1).pack()
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_member_add_options_keyboard(project_id, i18n: I18nContext):
    buttons = [
        [
            InlineKeyboardButton(
                text=i18n.get("projects-add-by-username"),
                callback_data=ProjectMemberAddCb(project_id=project_id, method="username").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=i18n.get("projects-add-by-contact"),
                callback_data=ProjectMemberAddCb(project_id=project_id, method="contact").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=i18n.get("common-back"), callback_data=ProjectViewCb(id=project_id).pack()
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def project_analytics_keyboard(project_id: str, i18n):

    builder = InlineKeyboardBuilder()

    builder.button(
        text=i18n.buttons.tasks(), callback_data=ProjectTasksCb(project_id=project_id).pack()
    )

    builder.button(
        text=i18n.buttons.members(), callback_data=ProjectMembersCb(project_id=project_id).pack()
    )

    builder.button(text=i18n.buttons.back(), callback_data=ProjectViewCb(id=project_id).pack())

    builder.adjust(2, 1)

    return builder.as_markup()
