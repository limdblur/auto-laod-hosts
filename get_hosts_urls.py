#!/usr/bin/python
#encoding:utf-8
'''
读取hosts_urls.txt来获得url地址
'''
config_file='hosts_urls_date.txt'

def get_hosts_urls():
    try:
        file_hosts_urls = open(config_file,'rU')
        address = file_hosts_urls.readline()
        if address==None or address==[]:
            print '读取hosts_urls.txt结果为空'
            return None
        if address[-1]=='\n':
            address=address[0:-1]
        update_date = file_hosts_urls.readline()
        if update_date==None or update_date==[]:
            print '读取hosts_urls.txt结果为空'
            return None
        if update_date[-1]=='\n':
            update_date=update_date[0:-1]
            
        file_hosts_urls.close()
        return (address,update_date)
    except Exception, e:
        print '读取hosts_urls.txt失败'
        return None


if __name__=='__main__':
    print get_hosts_urls()
