#!/usr/bin/python
#encoding:utf-8
import subprocess
import shlex
import platform
import os

def get_the_zipped_hosts_filename():
    system=platform.system()
    if system=='Linux':
        zipped_hosts_filename=u'Android安卓跟Linux系列.zip'
    else:
        zipped_hosts_filename=u'Windows系列跟苹果系列.zip'

    return zipped_hosts_filename


if __name__=='__main__':
    pass
