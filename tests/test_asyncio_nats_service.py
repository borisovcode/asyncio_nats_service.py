import unittest

from asyncio_nats_service.service import NatsServiceBase


class NatsService(NatsServiceBase):
    pass


class TestService(unittest.IsolatedAsyncioTestCase):
    svc: NatsServiceBase

    def setUp(self) -> None:
        self.svc = NatsService()

    def test_options(self):
        self.assertEqual(self.svc._nats_get_connection_string(), self.svc.NATS_SERVERS)


if __name__ == '__main__':
    unittest.main()
