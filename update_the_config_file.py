#!/usr/bin/python
#encoding:utf-8

CONFIG_FILENAME='hosts_urls_date.txt'
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
if __name__=='__main__':
    hostsfile_update_date='20160506'
    hostsfile_update_version=1
    update_the_config_file(hostsfile_update_date,hostsfile_update_version)
