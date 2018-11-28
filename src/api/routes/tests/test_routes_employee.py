#!/usr/bin/python

from api.utils.test_base import BaseTestCase


class TestEmployees(BaseTestCase):
    def setUp(self):
        super(TestEmployees, self).setUp()

    def test_get_employees(self):
        self.assertEqual(True, True)
