#!/usr/bin/python
#encoding:utf-8
import subprocess
import shlex
import platform
import os
'''
解压zip文件
'''
def get_the_zipped_hosts_filename():
    system=platform.system()
    if system=='Linux':
        zipped_hosts_filename='Android安卓跟Linux系列.zip'
    else:
        zipped_hosts_filename='Windows系列跟苹果系列.zip'

    return zipped_hosts_filename

def is_unzip_exists():
    try:
        if subprocess.call('unzip')==0:
            print '执行unzip成功'
            return True
    except:
        print '无法执行unzip命令'
        return False
    
def unzip_zipped_hosts_file(zippedfilename,passwd):
    is_unzip_exists()
    try:
        commandline='unzip'+' '+'-P'+' '+passwd+' '+'-f -qq'+' '+os.getcwd()+'/'+zippedfilename
        args=shlex.split(commandline)
        #print args
        if subprocess.check_call(args)==0:
            print '解压文件'+zippedfilename+'成功'
            return True
    except:
        print '解压文件'+zippedfilename+'失败：可能文件不存在'
        return False
   
if __name__=='__main__':
    zipped_hosts_filename=get_the_zipped_hosts_filename()
    unzip_zipped_hosts_file(zipped_hosts_filename,'nite')
