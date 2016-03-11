#!/usr/bin/python
#encoding:utf-8

import subprocess
import shlex
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
    clean_downloads()
