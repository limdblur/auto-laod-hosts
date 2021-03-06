#!/usr/bin/python
#encoding:utf-8
import httplib

import urllib2
from bs4 import BeautifulSoup
import re



#避免编码错误
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #http://wangye.org/blog/archives/629/

'''
需要获得的信息包括hosts文件的百度网盘地址，百度网盘共享密码，zip文件解压密码,hosts
文件的更新日期

urlparse.urlparse对url字符拆分成各个部件
url的结构是这样的：
协议://授权/路径;参数?连接符#拆分文档中的特殊锚
'''
    
def get_remote_hosts_file_info(hosts_address):
    (baiduwp_address,baiduwp_passwd,hosts_dir_name,\
    zipfile_passwd,hostsfile_update_date,hostsfile_update_version) =('','','','','',0)
    try:
        html_content=urllib2.urlopen(hosts_address,timeout=100).read()
        #print html_content
        #html_content=open('1.txt','r').read()
    except Exception, e:
        print e
        return ('','','','','',0)
#从content中获取信息
    try:
        soup_re = BeautifulSoup(html_content,"lxml")
        #print soup_re.find_all('p')
        for tagsobjects in soup_re.find_all('p'):
            strings=tagsobjects.get_text() #这里默认的是ascii编码
            print strings
            result=strings.find(u'百度网盘')
            if result!=-1:
                if strings.find(u'提取码')!=-1:
                    strings_we_want_lists = strings.split(u'腾讯微云')
                    if len(strings_we_want_lists)<2:
                        strings_we_want_lists = strings.split(u'360云盘') #增加360云盘标志
                        if len(strings_we_want_lists)<2:
                            strings_we_want_lists = strings.split(u'微云网盘') #增加360云盘标志
                    strings_we_want=strings_we_want_lists[0]
                    print strings,result
                    for href in tagsobjects.find_all('a'):
                        if href['href'].find('baidu')!=-1:
                            baiduwp_address=href['href'] #获得了baidu微盘的地址额
                            re_num = r'[0-9]+'
                            date_list=re.findall(re_num,href.get_text())
                            print date_list
                            hostsfile_update_date=date_list[0]
                            if len(date_list)!=1:
                                hostsfile_update_version=int(date_list[1])
                            else:
                                hostsfile_update_version=0
                            #print hostsfile_update_date
                    break
    except Exception,e:
        print e          #有可能会超时，这是需要注意的问题
        return ('','','','','',0)
#获取了对应的字符串，可以获得日期，提取码，解压密码
#test 百度网盘 20160311-hosts下载 提取码 ：jtr5  解码密码：jubaonimabi腾讯微云 20160311-hosts下载 提取码 ：jH6D  解码密码：jubaonimabi 0
#测试的时候还是应该进行单元测试
    re_splits=u'[： ]'
    result_list=re.split(re_splits,strings_we_want)
    #print result_list
    baiduwp_passwd=result_list[4]
    zipfile_passwd=result_list[6]
    #获取hosts_dir_name
    sep1_bdwp=strings_we_want.split(u'百度网盘')
    #print sep1_bdwp
    sep2_xz=sep1_bdwp[1].split(u'下载')[0]
    #print sep2_xz
    #消除前导空格与末尾空格
    remove_headblank=sep2_xz.lstrip(' ')
    remove_tailblank=remove_headblank.rstrip(' ')
    hosts_dir_name=remove_tailblank
    print hosts_dir_name
    return (baiduwp_address,baiduwp_passwd,hosts_dir_name,zipfile_passwd,hostsfile_update_date,hostsfile_update_version)


if __name__=='__main__':
    hosts_address='http://laod.cn/hosts/2016-google-hosts.html'
    print get_hosts_file_info(hosts_address)
