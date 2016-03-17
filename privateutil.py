#!/usr/bin/python
#encoding:utf-8
import subprocess
import shlex
import platform
import os

'''
读取hosts_urls.txt来获得url地址
'''
CONFIG_FILENAME='hosts_urls_date.txt'

def get_hosts_urls():
    try:
        file_hosts_urls = open(CONFIG_FILENAME,'rU')
        address = file_hosts_urls.readline()
        if address==None or address==[]:
            print '读取hosts_urls.txt结果为空'
            return None
        if address[-1]=='\n':
            address=address[0:-1]
        file_hosts_urls.close()
        return address
    except Exception, e:
        print '读取hosts_urls.txt失败'
        return None
        
def get_hosts_info_from_config_file():
    configfp=open(CONFIG_FILENAME)
    lines=configfp.readlines()
    update_date=lines[1].split(':')[1][0:-1]
    update_version=lines[2].split(':')[1][0:-1]
    if update_version[-1]=='\n':
        update_version=update_version[0:-1]
    configfp.close()
    return (update_date,int(update_version))

def update_the_config_file(hostsfile_update_date,hostsfile_update_version):
    read_update_config=open(CONFIG_FILENAME,'r')
    lines=read_update_config.readlines()
    index=0
    for line in lines:
        elements=line.split(':')
        if len(elements)==2:
            if elements[0]=='date':
                lines[index]='date'+':'+hostsfile_update_date+'\n'
            elif elements[0]=='version':
                lines[index]='version'+':'+str(hostsfile_update_version)+'\n'
            else:
                pass
        index+=1
    read_update_config.close()
    
    writefile=open(CONFIG_FILENAME,'w+')
    writefile.writelines(lines)
    writefile.close()
        
def get_the_zipped_hosts_filename():
    system=platform.system()
    if system=='Linux':
        zipped_hosts_filename=u'Android安卓跟Linux系列.zip'
    else:
        zipped_hosts_filename=u'Windows系列跟苹果系列.zip'

    return zipped_hosts_filename

def clean_downloads():
    command_line='rm -f *.zip hosts'
    args=shlex.split(command_line)
    try:
        subprocess.check_call(args)
        return True
    except Exception,e:
        print e
        return False
        
if __name__=='__main__':
    pass
