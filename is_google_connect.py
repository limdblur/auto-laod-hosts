#!/usr/bin/python
#encoding:utf-8

import subprocess
import shlex
'''
ping 太底层了，或许应该更加对症下药的测试HTTP request的连通性
Ping usage:
       If  ping  does  not  receive any reply packets at all it will exit with
       code 1. If a packet count and deadline are both  specified,  and  fewer
       than  count  packets are received by the time the deadline has arrived,
       it will also exit with code 1.  On other error it exits  with  code  2.
       Otherwise  it exits with code 0. This makes it possible to use the exit
       code to see if a host is alive or not.

       This program is intended for use in network  testing,  measurement  and
       management.   Because  of  the load it can impose on the network, it is
       unwise to use ping during normal operations or from automated scripts.

'''
BAIDUHOST='www.baidu.com'
GOOGLEHOST='www.google.com.hk'
FACEBOOKHOST='www.facebook.com'

def ping_test(host):
    command_line = 'ping -c 3 -W 5 '+host
    args = shlex.split(command_line)
    try:
        subprocess.check_call(args)
        #print "web server is up!"
        return True
    except subprocess.CalledProcessError:
        #print "Failed to get the host: %s." %host
        return False

def is_network_connected():
    result=ping_test(BAIDUHOST)
    if result:
        print '百度可以连接上，说明网络是连通的'
    else:
        print '百度连接不上，说明网络链接有问题，不一定是Google ip失效'

    return result

def is_google_connected():
    result=ping_test(GOOGLEHOST)
    if result:
        print 'Google可以连接上'
    else:
        print 'Google连接不上'

    return result


if __name__=='__main__':
    is_network_connected()
    is_google_connected()
    pass
