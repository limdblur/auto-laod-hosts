#!/usr/bin/python
#encoding:utf-8

'''
需要获得的信息包括hosts文件的百度网盘地址，百度网盘共享密码，zip文件解压密码,hosts
文件的更新日期
'''

def get_hosts_file_info(hosts_address):
    (baiduwp_address,baiduwp_passwd,\
    zipfile_passwd,hostsfile_update_date) =('','','','')
   
    return (baiduwp_address,baiduwp_passwd,zipfile_passwd,hostsfile_update_date)

if __name__=='__main__':
    hosts_address='http://laod.cn/hosts/2016-google-hosts.html'
    print get_hosts_file_info(hosts_address)
