#!/usr/bin/python
#encoding:utf-8

cookie_r=open('cookies.dat','r')
lines=cookie_r.readlines()
cookie_r.close()
cookie_w=open('cookies.dat','w')
index=0
for line in lines:
    lines[index]=lines[index].replace('\r\n','\n')
    index+=1
print lines
cookie_w.writelines(lines)
cookie_w.close()
