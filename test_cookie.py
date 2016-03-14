#!/usr/bin/python
#encoding:utf-8

import urllib2
import urlparse
import requests
import httplib
import cookielib

filename='cookies.txt'

cookie=cookielib.MozillaCookieJar(filename)
handler=urllib2.HTTPCookieProcessor(cookie)
opener=urllib2.build_opener(handler)
response=opener.open("http://www.baidu.com")

cookie.save(ignore_discard=True,ignore_expires=True)
