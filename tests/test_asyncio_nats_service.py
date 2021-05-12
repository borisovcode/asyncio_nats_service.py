import unittest

from service import NatsServiceBase


class TestService(unittest.IsolatedAsyncioTestCase):
    svc: NatsServiceBase

    def setUp(self) -> None:
        self.svc = NatsServiceBase()

    def test_options(self):
        self.assertEqual(self.svc._nats_get_connection_string(), self.svc.NATS_SERVERS)


if __name__ == '__main__':
    unittest.main()
