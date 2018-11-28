#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from api.utils.factory import create_app
from api.utils.database import db
from api.utils.config import TestingConfig
import os


class BaseTestCase(unittest.TestCase):
    """A base test case"""
    def setUp(self):
        if os.environ.get('WORK_ENV') == 'PROD':
            app = create_app(TestingConfig)
            app.app_context().push()
            self.app = app.test_client()

    def tearDown(self):
        if os.environ.get('WORK_ENV') == 'PROD':
            db.session.close_all()
            db.drop_all()
