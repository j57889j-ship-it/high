from aiogram import Router

from . import books, help, leaderboard, navigation, profile, quiz, start


def build_router() -> Router:
    router = Router(name="user")
    for module in (start, books, quiz, profile, leaderboard, help, navigation):
        router.include_router(module.router)
    return router
