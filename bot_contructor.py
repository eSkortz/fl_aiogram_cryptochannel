# * не используется в этом проекте, но очень удобный конструктор

from functools import singledispatchmethod
from typing import List

from aiogram import Bot, Dispatcher, Router


class BotConstructor:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(BotConstructor, cls).__new__(cls)
        return cls.instance

    def __init__(self, dp: Dispatcher, bot: Bot):
        self.dp = dp
        self.bot = bot

    @singledispatchmethod
    def set_router(self, router: List[Router] or Router) -> None:
        raise NotImplementedError(f'Cannot format value of type {type(router)}')

    @set_router.register
    def _(self, routers: list) -> None:
        for router in routers:
            self.dp.include_router(router)

    @set_router.register
    def _(self, router: Router) -> None:
        self.dp.include_router(router)

    async def start_polling(self) -> None:
        await self.dp.start_polling(
            self.bot,
            handle_as_tasks=True,
            allowed_updates=self.dp.resolve_used_update_types(),
        )

    async def __set_webhook(self, webhook_url: str) -> None:
        await self.bot.set_webhook(
            url=webhook_url,
            allowed_updates=self.dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )

        await self.bot.session.close()

    async def start_webhook(self, webhook_url: str) -> None:
        await self.bot.delete_webhook()
        await self.bot.get_updates(offset=-1)
        await self.__set_webhook(webhook_url)
