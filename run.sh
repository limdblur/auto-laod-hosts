#!/bin/bash
#pip install bs4 requests pillow
#brew install wget libjpeg git
#增加一个参数forced，可以强制升级
CODEPATH=$HOME/pythonpractice/python-network/hosts-auto-update
PASSWD=root
cd $CODEPATH
echo $PASSWD|sudo -S python auto_update_main.py $1
