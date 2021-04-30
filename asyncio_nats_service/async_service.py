import asyncio


class AsyncServiceMixin(object):
    """
    Примесь для создания сервисов с асинхронным кодом
    """
    async_loop: asyncio.AbstractEventLoop = None

    @classmethod
    def async_init(cls):
        """Инициализация асинхронного кода - петли"""
        if cls.async_loop is None:
            cls.async_loop = asyncio.get_event_loop()
        return cls.async_loop

    def async_run_until_complete(self, async_entry_point=None):
        """
        Стандартный запуск асинхронного сервиса

        :param async_entry_point: точка входа
        """
        if self.async_loop is None:
            self.async_init()

        if async_entry_point:
            entry_point = async_entry_point
        elif isinstance(self, AsyncServiceMixin):
            entry_point = self.run_async
        else:
            raise UnboundLocalError

        self.async_loop.run_until_complete(entry_point())

        try:
            self.async_loop.run_forever()
        finally:
            self.async_loop.close()

    def async_create_task(self, *args, **kwargs):
        """Обёртка для добавления задачи"""
        return self.async_loop.create_task(*args, **kwargs)

    async def run_async(self):
        """Стандартная точка входа в асинхронный сервис"""
        pass
