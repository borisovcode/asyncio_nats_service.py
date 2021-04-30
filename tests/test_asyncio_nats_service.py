# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from service import NatsServiceBase


class TestService(unittest.TestCase):
    svc: NatsServiceBase

    def setUp(self) -> None:
        self.svc = NatsServiceBase()

    def test_options(self):
        self.assertEqual(self.svc._nats_get_connection_string(), self.svc.NATS_SERVERS)


if __name__ == '__main__':
    unittest.main()
