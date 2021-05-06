import inspect

from nats.aio.client import Client as NatsClient

from __version__ import __version__  # noqa
from argument_parser import ArgumentParserMixin
from async_service import AsyncServiceMixin
from logger import LoggerMixin
from msgpack import MsgPackMixin
from subscribers import NatsSubscriberBase

__lang__ = 'python3'


class NatsServiceBase(ArgumentParserMixin, MsgPackMixin, LoggerMixin, AsyncServiceMixin):
    """
    Базовый класс для работы с NATS

    Добавляется параметр командной строки --nats-servers.
    Оборачиваются функции publish и subscribe для NATS, при это для подписки автоматически может формироваться имя обработчика.

    Пример:

        svc = NetcatService()
        svc.async_run_until_complete()

    """

    NATS_SERVERS = ['nats://localhost:4333', ]

    """Перечень обработчиков для тем сообщений"""
    _nats_subject_handler = {}

    """Параметры соединения клиента, включая обработчики"""
    _nats_options = {}

    """Собственно клиент NATS"""
    nats_client = NatsClient()

    def _nats_get_connection_string(self):
        return self.argument_parser_options.nats_servers

    async def _nats_error_handler(self, e):
        """Обработчик ошибок NATS по-умолчанию"""
        self._logger.error(f'{type(e).__name__} {e}')

    async def _nats_closed_handler(self):
        """Обработчик закрытия NATS по-умолчанию"""
        self._logger.debug("Connection to NATS is closed.")

    async def _nats_reconnected_handler(self):
        """Обработчик повторного соединения к NATS по-умолчанию"""
        self._logger.debug(f"Connected to NATS at {self.nats_client.connected_url.netloc}...")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Добавить аргумент командной строки --nats-servers nats://<host>:<port>"""
        self.argument_parser_add('--nats-servers', default=self.NATS_SERVERS, action='append')
        options = {
            'servers': self._nats_get_connection_string(),
            'error_cb': self._nats_error_handler,
            'closed_cb': self._nats_closed_handler,
            'reconnected_cb': self._nats_reconnected_handler
        }
        self._nats_options = options

    def _nats_get_handler(self, subject):
        """
        Получение обработчика для темы сообщения

        - Если тема есть в специальном словаре _nats_subject_handler, то брать оттуда.
          - Если там указан класс, который инициализируется с параметрами nats_client и async_loop, обработчик - метод message_handler
          - Если там указана функция, то брать её
        - Если нет, то заменить все . на _, вместо * писать __star__, вместо > писать __next__,
          впереди добавить _nats_handler_
        """
        if subject in self._nats_subject_handler:
            if isinstance(self._nats_subject_handler[subject], NatsSubscriberBase):
                obj = self._nats_subject_handler[subject](nats_client=self.nats_client, async_loop=self.async_loop)
                self._nats_subject_handler[subject] = obj.message_handler
            elif inspect.isfunction(self._nats_subject_handler[subject]):
                handler = self._nats_subject_handler[subject]
            else:
                raise TypeError(f'unknown "{subject}" handler (may be a function or a NatsScribeBase subclass')
        else:
            handler_name = '_nats_handler_' + subject.replace('.', '_').replace('*', '__star__').replace('>', '__next__')
            handler = getattr(self, handler_name)
        return handler

    async def nats_subscribe(self, subject, queue='', handler=None):
        """
        Добавление подписки на сообщения NATS

        :param subject: тема сообщения, например 'my.task'
        :param queue: название очереди сообщений для горизонтального масштабирования
        :param handler: обработчик (callback функция)
        :return: ssid подписки
        """
        if handler is None:
            handler = self._nats_get_handler(subject)
        await self.nats_client.subscribe(subject, queue, cb=handler)

    async def _nats_subscribe(self, *args, **kwargs):
        """Обёртка для подписки (получения сообщений) NATS"""
        return await self.nats_client.subscribe(*args, **kwargs)

    async def _nats_publish(self, *args, **kwargs):
        """Обёртка для публикации (отправки сообщения) NATS"""
        return await self.nats_client.publish(*args, **kwargs)

    async def nats_publish(self, *args, **kwargs):
        """Публикация (отправка сообщений) NATS"""
        return await self._nats_publish(*args, **kwargs)

    async def run_async(self):
        """Точка входа в асинхронный сервис"""
        await super().run_async()
        self._nats_options['servers'] = self._nats_get_connection_string()
        await self.nats_client.connect(**self._nats_options)
