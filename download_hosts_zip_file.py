#!/usr/bin/python
#encoding:utf-8
import urllib2
import urlparse
import requests
import httplib

class HTTPClient:

    def __init__(self, host):
        self.host = host

    def fetch(self, path):
        http = httplib.HTTP(self.host)

        # Prepare header
        http.putrequest("GET", path)
        http.putheader("User-Agent", 'Mozilla')
        http.putheader("Host", self.host)
        http.putheader("Accept", "*/*")
        http.endheaders()

        try:
            errcode, errmsg, headers = http.getreply()

        except Exception, e:
                print "Client failed error code: %s message:%s headers:%s" %(errcode, errmsg, headers)
        else: 
            print "Got homepage from %s" %self.host 

        file = http.getfile()
        return file.read()
    
def get_hosts_file_info1(hosts_address):
    parse_re = urlparse.urlparse(hosts_address)
    hosts = parse_re.netloc
    path=parse_re.path
    #print hosts,path
    client = HTTPClient(hosts)
    content = client.fetch(path)
    print content
    
def download_hosts_zip_file(baiduwp_address,baiduwp_passwd,hosts_dir_name):
    #step 0：短url的处理,baidu网盘估计禁止爬虫，那么可以模拟浏览器 
    parse_re = urlparse.urlparse(baiduwp_address)
    hosts = parse_re.netloc
    print hosts
    path=parse_re.path
    headers = [('Host',hosts),
    ('Connection', 'keep-alive'),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'),
    ('Accept-Encoding','gzip,deflate'),
    ('Accept-Language', 'en-US,en;q=0.5'),
    ('Referer','http://laod.cn/hosts/2016-google-hosts.html')]
    #可能需要构造特殊的cookie
    opener = urllib2.build_opener()
    opener.addheaders = headers
    data = opener.open(baiduwp_address).read()
    print data
    #step 1：是否需要处理cookie
    #输入提取码
    
    #step 2：是否需要处理cookie
    #进入下一级目录

    #step 3：需要了解js是怎么动作的，因为链接不是直接在页面中而是动态生产的
    #获取待下载zip文件的链接

    #step 4
    #使用wget下载zip文件

if __name__=='__main__':
    baiduwp_address,baiduwp_passwd,hosts_dir_name=\
                                                    'http://pan.baidu.com/s/1nu0OV3N',\
                                                    'hsmi',\
                                                    '20160311-v3'
    download_hosts_zip_file(baiduwp_address,baiduwp_passwd,hosts_dir_name)
