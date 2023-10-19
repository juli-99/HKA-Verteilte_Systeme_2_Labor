"""
Simple client server unit test
"""

import logging
import random
import threading
import unittest
import math

import sol_clientserver
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestPhoneNumberServer(unittest.TestCase):
    """The test"""
    _server = sol_clientserver.Server()  # create single server in class variable
    _server.add_entry('Philip', 12345678901)

    for _ in range(499):
        _server.add_entry(
            ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6)),
            math.floor(random.random() * 999999999)
        )

    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = sol_clientserver.Client()  # create new client for each test

    def test_srv_get_ex(self):  # each test_* function is a test
        """Test get for existing key"""
        msg = self.client.get('Philip')
        self.assertEqual(msg, '12345678901')

    def test_srv_get_un(self):
        msg = self.client.get('Phili')
        self.assertEqual(msg, 'unknown key')

    def test_get_all(self):
        msg = self.client.get_all()
        self.assertEqual(msg.count('\n'), 500)

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate


if __name__ == '__main__':
    unittest.main()
