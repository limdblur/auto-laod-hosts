#!/usr/bin/python
#encoding:utf-8
import urllib
import urllib2
import urlparse
import requests
import httplib
import cookielib
import requests
import re
import json
import os
import privateutil
import the_gui
import shlex
import subprocess
try:
    from urllib import unquote as url_unquote
except ImportError:
    from urllib.parse import unquote as url_unquote
from time import time

#避免编码错误
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #http://wangye.org/blog/archives/629/

DLTYPE_MULTIPLE = u'multi_file'
class ShareInfo(object):
    pattern = re.compile('yunData\.(\w+\s=\s"\w+");')
    filename_pattern = re.compile('"server_filename":"([^"]+)"', re.DOTALL)
    fileinfo_pattern = re.compile('yunData\.FILEINFO\s=\s(.*);')

    def __init__(self):
        self.share_id = None
        self.bdstoken = None
        self.uk = None
        self.bduss = None
        self.fid_list = None
        self.sign = None
        self.filename = None
        self.timestamp = None
        self.sharepagetype = None
        self.fileinfo = None
        self.sekey=None
    def __call__(self, js):
        return self.match(js)

    def __repr__(self):
        return '<ShareInfo %r>' % self.share_id

    def match(self, js):
        _filename = re.search(self.filename_pattern, js)
        _fileinfo = re.search(self.fileinfo_pattern, js)
        if _filename:
            self.filename = _filename.group(1).decode('unicode_escape')
        if _fileinfo:
            self.fileinfo = json.loads(_fileinfo.group(1).decode('unicode_escape'))
        data = re.findall(self.pattern, js)
        if not data:
            return False
        yun_data = dict([i.split(' = ', 1) for i in data])
        #logger.debug(yun_data, extra={'method': 'GET', 'type': 'javascript'})
        #if 'single' not in yun_data.get('SHAREPAGETYPE') or '0' in yun_data.get('LOGINSTATUS'):
        #    return False
        self.uk = yun_data.get('SHARE_UK').strip('"')
        # self.bduss = yun_data.get('MYBDUSS').strip('"')
        self.share_id = yun_data.get('SHARE_ID').strip('"')
        self.fid_list = json.dumps([i['fs_id'] for i in self.fileinfo])
        self.sign = yun_data.get('SIGN').strip('"')
        if yun_data.get('MYBDSTOKEN'):
            self.bdstoken = yun_data.get('MYBDSTOKEN').strip('"')
        self.timestamp = yun_data.get('TIMESTAMP').strip('"')
        self.sharepagetype = yun_data.get('SHAREPAGETYPE').strip('"')
        if self.sharepagetype == DLTYPE_MULTIPLE:
            self.filename = os.path.splitext(self.filename)[0] + '-batch.zip'
        #if self.bdstoken:
        #    return True
        self.fileinfo=self.fileinfo[0]
        return True

def _get_js(opener,link, secret=None):
    """Get javascript code in html which contains share files info
    :param link: netdisk sharing link(publib or private).
    :type link: str
    :return str or None
    """
    req = urllib2.Request(link)
    data = opener.open(req).read()
    js_pattern = re.compile('<script\stype="text/javascript">!function\(\)([^<]+)</script>', re.DOTALL)
    js = re.findall(js_pattern, data)
    return js[0] or None
    
def download_hosts_zip_file(baiduwp_address,baiduwp_passwd,hosts_dir_name):
    #step 0：短url的处理,baidu网盘估计禁止爬虫，那么可以模拟浏览器，需要cookie
   
    parse_re = urlparse.urlparse(baiduwp_address)
    hosts = parse_re.netloc
    #print hosts
    path=parse_re.path
    referer1='http://laod.cn/hosts/2016-google-hosts.html'
#https://www.douban.com/group/topic/18095751/
#如果encoding是gzip的话，会导致传输回来的网页是压缩格式的，一堆乱码
    headers = [('Host',hosts),
    ('Connection', 'keep-alive'),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'),
    #('Accept-Encoding','gzip,deflate'), 
    ('Accept-Language', 'en-US,en;q=0.5'),
    ('Referer',referer1)]
    
    #可能需要构造特殊的cookie
    try:
        cookie_filename='cookies.txt'
        #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
        cookie=cookielib.MozillaCookieJar(cookie_filename)
        #cookie.load('cookies.dat',ignore_discard=True,ignore_expires=True)

        handler=urllib2.HTTPCookieProcessor(cookie)
    
        req=urllib2.Request(baiduwp_address)
        first_opener = urllib2.build_opener(handler)
        first_opener.addheaders = headers
        first_opener.open(req)
    except Exception,e:
        print e
        
    for item in cookie:
        print 'Name = '+item.name
        print 'Value = '+item.value
    cookie.save(ignore_discard=True,ignore_expires=True)
    #利用cookie请求再次访问同一个地址，这里会有一个重定向
    sencond_data=first_opener.open(req)
    #print sencond_data.read()
    for item in cookie:
        print 'Name = '+item.name
        print 'Value = '+item.value
    cookie.save(ignore_discard=True,ignore_expires=True)
    
    #print data
    #step 1：是否需要处理cookie
    #更改Rederer
    referer2=sencond_data.geturl()
    print 'referer2 is',referer2
    headers[-1]=('Referer',referer2)
    #first_opener.addheaders = headers #更新头部
    #req2=urllib2.Request(referer2)
    #输入提取码
    url2='http://pcs.baidu.com/rest/2.0/pcs/file?method=plantcookie&type=ett'
    req2=urllib2.Request(url2)
    #first_opener.addheaders = headers
    first_opener.open(req2)
    cookie.save(ignore_discard=True,ignore_expires=True)
    for item in cookie:
        print 'Name = '+item.name
        print 'Value = '+item.value

    data_post3={'pwd':baiduwp_passwd,'vcode':'','vcode_str':''}
    data_post3_encode=urllib.urlencode(data_post3)
    print data_post3_encode
    url3="{0}&t={1}&".format(referer2.replace('init','verify'),str(int(time())))
    print 'url3 is',url3
    req3=urllib2.Request(url3,data_post3_encode)
    jsonmsg=json.loads(first_opener.open(req3).read())
    cookie.save(ignore_discard=True,ignore_expires=True)

    print jsonmsg,type(jsonmsg) #got request_id
    errno=jsonmsg['errno']
    if errno == -63:
        print '提取密码遇到要输入验证码'
        while True:
            errno=yanzhengmashuru(first_opener,baiduwp_passwd,referer2)
            if errno==0:
                break
        
    elif errno == -9:
        print 'VerificationError("提取密码错误\n")'
        raise UnknowError
    elif errno == 0:
        pass
    else:
        print '提取密码遇到UnknownError'
        raise UnknowError        

    js = _get_js(first_opener,baiduwp_address, baiduwp_passwd)
    #print js

    info=ShareInfo()
    if info.match(js):
        print info.filename
        if info.sharepagetype == DLTYPE_MULTIPLE:
            print info.fileinfo
            dirname=info.fileinfo[u'path']
            print dirname
        url4="{0}&".format(referer2.replace('init','list')) #返回目录下的文件列表
        data_get_req={
            'dir':dirname,
            'page':1
            }
        data_get_req_encode=urllib.urlencode(data_get_req)
        url4+=data_get_req_encode
        print 'url4 is',url4
        req4=urllib2.Request(url4)
        returned_filelistinfo=json.loads(first_opener.open(req4).read())

        errno=returned_filelistinfo[u'errno']
        zipped_filename=privateutil.get_the_zipped_hosts_filename() #获取对应系统平台的文件名字
        print zipped_filename
        if errno==0:
            #get SHARE_ID,SEKEY,SIGN,SHARE_UK
            share_id=info.share_id
            share_uk=info.uk
            sign=info.sign
            print 'sign is',sign
            sekey=info.sekey #暂时为None
            sekey='{"sekey":"%s"}' % (url_unquote(u'f9ciJq7HsoXeVjfiJjgrYn%2FppjvK7p8uETVQzEZBfxQ%3D'))
            timestamp=info.timestamp
            bdstoken=info.bdstoken

            #server_filename
            #fs_id
            filelistinfo=returned_filelistinfo[u'list']
            for eachfileinfo in filelistinfo:
                if eachfileinfo['server_filename']==zipped_filename:
                    fid_list=[eachfileinfo['fs_id']]
                    print 'fid_list is',fid_list
            url5='http://pan.baidu.com/api/sharedownload?'
            data_get_req5={
                'sign':sign,
                'timestamp':timestamp,
                'bdstoken':bdstoken,
                }
            data_get_req5_encode=urllib.urlencode(data_get_req5)
            print 'data_get',data_get_req5
            url5+=data_get_req5_encode
            print 'url5 is',url5
            data_post5={
                'encrypt':'0',
                'extra':sekey,
                'fid_list':fid_list,
                'product':'share',
                'primaryid':share_id,
                'uk':share_uk,
                'vcode_input':'',
                'vcode_str':''
                }
            data_post5_encode=urllib.urlencode(data_post5)
            while True:
                print 'data_post5',data_post5
                req5=urllib2.Request(url5,data_post5_encode)
                returned_info=first_opener.open(req5).read()

                print returned_info
                returned_jsoninfo=json.loads(returned_info)
                print '返回值5',returned_jsoninfo
                if returned_jsoninfo['errno']==0:
                    download_link=returned_jsoninfo[u'list'][0][u'dlink']
                    print 'dlink is',download_link
                    break
                elif returned_jsoninfo['errno']==-20 or returned_jsoninfo['errno']==2:
                    #获取vcode image
                    #http://pan.baidu.com/api/getcaptcha?prod=shareverify&web=1&t=0.5653103908215448&channel=chunlei&clienttype=0&web=1
                    url6=u'http://pan.baidu.com/api/getcaptcha?'
                    data_get_req6={
                        'prod':'shareverify',
                        }
                    if bdstoken:
                        data_get_req6['bdstoken']=bdstoken
                    data_get_req6_encode=urllib.urlencode(data_get_req6)
                    url6+=data_get_req6_encode
                    print 'url6 is',url6
                    req6=urllib2.Request(url6)
                    returned_jsoninfo=json.loads(first_opener.open(req6).read())
                    errno=returned_jsoninfo['errno']
                    print errno
                    if errno==0:
                        vcode_str=returned_jsoninfo['vcode_str']
                        print vcode_str
                        vcode_img_url=returned_jsoninfo['vcode_img']
                        print vcode_img_url

                        url7=vcode_img_url
                        req7=urllib2.Request(url7)
                        imgdata=first_opener.open(req7).read()
                        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), u'vcode.jpg')
                        with open(img_path, mode='wb') as fp:
                            fp.write(imgdata)
                        print("Saved verification code to ", os.path.dirname(os.path.abspath(__file__)))
                        #输入vcode
                        the_gui.input_vcode(u'vcode.jpg')
                        vcode_text=the_gui.global_vcode
                        print vcode_text
                        #更新data_post5
                        data_post5['vcode_input']=vcode_text
                        data_post5['vcode_str']=vcode_str
                        data_post5_encode=urllib.urlencode(data_post5)
                        #传输验证
                        #data_post8={'pwd':baiduwp_passwd,'vcode':vcode_text,'vcode_str':vcode_str}
                        #data_post8_encode=urllib.urlencode(data_post8)
                        #print data_post8_encode
                        #url8="{0}&t={1}&".format(referer2.replace('init','verify'),str(int(time())))
                        #print url8
                        #req8=urllib2.Request(url8,data_post8_encode)
                        #jsonmsg=json.loads(first_opener.open(req8).read())
                        #errno=jsonmsg['errno']
                        #print errno
                        
                        #继续循环
                        continue
                    else:
                        raise UnknowError
                    
                else:
                    print 'errno is',returned_jsoninfo['errno']
                    raise UnknowError
    #step 2：是否需要处理cookie
    #进入下一级目录

    #step 3：需要了解js是怎么动作的，因为链接不是直接在页面中而是动态生产的
    #获取待下载zip文件的链接
    print '我们获得了下载链接',download_link
    #step 4
    #使用wget下载zip文件
    #这一步也需要使用cookie
    commandline='wget --cookies=on --load-cookies=cookie.txt --keep-session-cookies --save-cookies=cookies.txt '+\
                 ' --referer='+referer2+'  '+download_link+'  '+'-O '+ zipped_filename
    args=shlex.split(commandline)
    result=subprocess.check_call(args)
    print 'wget result is',result
    if result==0:
        return True
    else:
        return False
    
def yanzhengmashuru(first_opener,baiduwp_passwd,referer2):
    #获取vcode image
    #http://pan.baidu.com/api/getcaptcha?prod=shareverify&web=1&t=0.5653103908215448&channel=chunlei&clienttype=0&web=1
    url6=u'http://pan.baidu.com/api/getcaptcha?'
    data_get_req6={
        'prod':'shareverify',
        }
    if bdstoken:
        data_get_req6['bdstoken']=bdstoken
    data_get_req6_encode=urllib.urlencode(data_get_req6)
    url6+=data_get_req6_encode
    print 'url6 is',url6
    req6=urllib2.Request(url6)
    returned_jsoninfo=json.loads(first_opener.open(req6).read())
    errno=returned_jsoninfo['errno']
    print errno
    if errno==0:
        vcode_str=returned_jsoninfo['vcode_str']
        print vcode_str
        vcode_img_url=returned_jsoninfo['vcode_img']
        print vcode_img_url

        url7=vcode_img_url
        req7=urllib2.Request(url7)
        imgdata=first_opener.open(req7).read()
        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vcode.jpg')
        with open(img_path, mode='wb') as fp:
            fp.write(imgdata)
        print("Saved verification code to ", os.path.dirname(os.path.abspath(__file__)))
        #输入vcode
        the_gui.input_vcode()
        vcode_text=the_gui.global_vcode
        #传输验证
        data_post8={'pwd':baiduwp_passwd,'vcode':vcode_text,'vcode_str':vcode_str}
        data_post8_encode=urllib.urlencode(data_post8)
        print data_post8_encode
        url8="{0}&t={1}&".format(referer2.replace('init','verify'),str(int(time())))
        print url8
        req8=urllib2.Request(url8,data_post8_encode)
        jsonmsg=json.loads(first_opener.open(req8).read())
        errno=jsonmsg['errno']
        print errno
        return errno
        
class UnknowError(Exception):
    pass

if __name__=='__main__':
    baiduwp_address,baiduwp_passwd,hosts_dir_name=\
                                                    'http://pan.baidu.com/s/1nu0OV3N',\
                                                    'hsmi',\
                                                    '20160311-v3'
    #baiduwp_address='http://pan.baidu.com'
    download_hosts_zip_file(baiduwp_address,baiduwp_passwd,None)
