# Author: Brandon Hamilton <brandon.hamilton@gmail.com>
# Copyright (c) 2015 Brandon Hamilton

# MIT License

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

__version__ = '0.1.0'
__author__ = 'Brandon Hamilton <brandon.hamilton@gmail.com>'
__copyright__ = "Copyright (c) 2015 Brandon Hamilton"
__license__ = "MIT"

import os
import requests

BASE_URI = 'https://updown.io/api/checks'

API_KEY = 'UPDOWN_API_KEY' in os.environ and os.environ['UPDOWN_API_KEY'] or None

def _performRequest(method, uri='', data=None):
    kwargs = { 'headers': { 'X-API-KEY' : API_KEY } }
    if data:
        kwargs['data'] = data
    r = requests.request(method, BASE_URI + uri, **kwargs)
    r.raise_for_status()
    return r.json()

def checks():
    r = _performRequest('GET')
    return { c['url'] : Check._fromObject(c) for c in r }

def add(url, period=60, apdex_t=0.25, enabled=True, published=False):
    c = Check(url, period, apdex_t, enabled, published)
    c.sync()
    return c

class Check:
    def __init__(self, url, period=60, apdex_t=0.25, enabled=True, published=False):
        self.token = None
        self.url = url
        self.period = period
        self.apdex_t = apdex_t
        self.enabled = enabled
        self.published = published

    @staticmethod
    def _fromObject(obj):
        c = Check(obj['url'])
        for attr, value in obj.items():
            setattr(c, attr, value)
        return c

    def _toObject(self):
        return { attr: getattr(self, attr) for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__") }

    def sync(self):
        if self.token:
            r = _performRequest('PUT', uri='/' + self.token, data=self._toObject())
            for attr, value in r.items():
                setattr(self, attr, value)
        else:
            r = _performRequest('POST', data=self._toObject())
            for attr, value in r.items():
                setattr(self, attr, value)

    def delete(self):
        if self.token:
            r = _performRequest('DELETE', uri='/' + self.token)
            return r['deleted']
        else:
            return True

    def downtimes(self, page=1):
        r = _performRequest('GET', '/' + self.token + '/downtimes', data={'page':page})
        return r

    def __repr__(self):
        return repr(self._toObject())

    def __str__(self):
        return str(self._toObject())
