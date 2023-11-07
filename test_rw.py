# coding=utf-8

import unittest

from order import OrderHandler


class TestLogin(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = None

    def setUp(self):
        pass

    def _main(self):        
        OrderHandler().run()

    def test_it(self):
        self._main()

    def tearDown(self):
        pass
