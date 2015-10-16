#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
Propose: 
Author: 'yac'
Date: 
"""

import urllib2
import json


class BaseHttpClient(object):
    """Implement http client """

    def __init__(self, base_url):

        self.base_url = base_url
        self.params = None

    def request(self, url, to_json=False):
        """ Make POST or GET http request """

        # POST
        if self.params:
            if to_json:
                self.params = json.loads(self.params)
            req = urllib2.Request(self.base_url+url, self.params, {'Content-Type': 'application/x-www-form-urlencoded'})
        else:  # GET
            req = urllib2.Request(self.base_url+url)

        try:
            file_object = urllib2.urlopen(req)
        except urllib2.URLError:
            return False, 'No server response'

        data = file_object.read()

        try:
            return json.loads(data)
        except ValueError:
            pass

        return data