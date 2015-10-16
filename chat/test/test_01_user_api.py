#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
Propose: 
Author: 'yac'
Date: 
"""
import os
import sys
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(APP_DIR, '../..'))

import unittest
from http_client import BaseHttpClient
from config import PORT, HOST

BASE_URL = 'http://%s:%s' % (HOST, PORT)

class TestUserAPI(unittest.TestCase):
    def test_01_create_user(self):

        client = BaseHttpClient(BASE_URL)
        client.params = 'username=test123455&password=111111&password_confirm=111111'

        # OK
        data = client.request('/signup')

        self.assertEqual(data['success'], True)
        # login is present
        data = client.request('/signup')
        self.assertEqual(data['errorMessage'], 'username exist')


    def test_02_login_logout_user(self):

        client = BaseHttpClient(BASE_URL)
        client.params = 'username=&password='

        data = client.request('/login')
        self.assertEqual(data['errorMessage'], 'empty login/password')

        client.params = 'username=dddddd&password=sadasdas'
        data = client.request('/login')
        self.assertEqual(data['errorMessage'], 'incorrect login/password')

        # OK
        client.params = 'username=test123455&password=111111'
        self.assertEqual(data['errorMessage'], 'incorrect login/password')

        # logout
        client.params = ''
        client.request('/logout')

if __name__ == '__main__':
    unittest.main()