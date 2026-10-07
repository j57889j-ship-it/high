from aiogram import Router

from . import channels, content, dashboard, leaderboard, quiz, settings, users


def build_router() -> Router:
    router = Router(name="admin")
    for module in (dashboard, content, users, channels, leaderboard, quiz, settings):
        router.include_router(module.router)
    return router
