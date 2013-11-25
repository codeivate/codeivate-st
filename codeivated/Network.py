'''
https://github.com/condemil/Gist/blob/master/gist.py
'''
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import os
import sys
import json
import base64
import subprocess
import functools


# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__) + "/..")
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)

# linux only works with v2.0.0 (v2.0.1 breaks it)
import requests


import tempfile
import traceback
import contextlib
import shutil
import re
import codecs

from . import Prefs

PY3 = sys.version > '3'

if PY3:
    import urllib.request as urllib
    import urllib.parse as urllib_parse
else:
    import urllib2 as urllib



class SimpleHTTPError(Exception):
    def __init__(self, code, response):
        self.code = code
        self.response = response


def catch_errors(fn):
    @functools.wraps(fn)
    def _fn(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except subprocess.CalledProcessError as err:
            sublime.error_message("Codeivate: Error with cURL returned %d" % err.returncode)
        except EnvironmentError as err:
            traceback.print_exc()
            if type(err) == OSError and err.errno == 2 and api_request == api_request_curl:
                sublime.error_message("Codeivate: Unable to find Python SSL module or cURL")
            else:
                msg = "Codeivate: Error while contacting API"
                if err.strerror:
                    msg += err.strerror
                sublime.error_message(msg)
        except SimpleHTTPError as err:
            msg = "Codeivate: site returned error %d" % err.code
            try:
                response_json = json.loads(err.response.decode('utf8'))
                response_msg = response_json.get('message')
                if response_msg:
                    msg += ": " + response_msg
            except ValueError:
                pass
            sublime.error_message(msg)
        except:
            traceback.print_exc()
            sublime.error_message("Codeivate: unknown error please report to http://codeivate.userecho.com")

    return _fn

@catch_errors
def api_request_urllib(url, raw_data=None, method=None):
    
    request = urllib.Request(url)
    print('API request url:', request.get_full_url())
    if method:
        request.get_method = lambda: method

    if raw_data is not None:
        request.add_header("Content-type", "application/x-www-form-urlencoded")
        data = urllib_parse.urlencode(raw_data).encode('utf-8')
        
        if PY3:
            # request.add_data(bytes(data, 'utf8'))
            request.add_data(data)
        else:
            request.add_data(data)

    print('API request data:', request.get_data())
    print('API request header:', request.header_items())
    if Prefs.proxies:
        opener = urllib.build_opener(urllib.HTTPHandler(), urllib.HTTPSHandler(),
                                     urllib.ProxyHandler(proxies))

        urllib.install_opener(opener)

    try:
        with contextlib.closing(urllib.urlopen(request)) as response:
            if response.code == 204:  # No Content
                return None
            else:
                return json.loads(response.read().decode('utf8', 'ignore'))

    except urllib.HTTPError as err:
        with contextlib.closing(err):
            raise SimpleHTTPError(err.code, err.read())



'''
Second attempt this is using requests module
http://www.python-requests.org/en/latest/user/quickstart/#make-a-request

proxies = {
  "http": "10.10.1.10:3128",
  "https": "10.10.1.10:1080",
}

requests.get("http://example.org", proxies=proxies)
To use HTTP Basic Auth with your proxy, use the http://user:password@host.com/ syntax:

proxies = {
    "http": "http://user:pass@10.10.1.10:3128/"
}

http://stackoverflow.com/questions/8287628/proxies-with-python-requests-module
'''
def api_request_requests(url, raw_data=None, method=None):
    # I haven't set proxies None and done away with these if statements because im not sure if it
    # will override environment proxy vars
    if raw_data is not None:
        if Prefs.proxies:
            r = requests.post(url, data=raw_data, proxies=Prefs.proxies)
            print("using proxy")
        else :
            r = requests.post(url, data=raw_data)
    else :
        if Prefs.proxies:
            r = requests.get(url, proxies=Prefs.proxies)            
            print("using proxy")
        else :
            r = requests.get(url)

    print("RESPONSE")        
    print(r)        
    return r.json()



api_request = api_request_requests