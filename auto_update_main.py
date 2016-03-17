#!/usr/bin/python
#encoding:utf-8

import sys
import get_hosts_file_info
import update_origin_hosts_file
import privateutil
import is_google_connect
import download_hosts_zip_file
import unzip_hosts_zip_file

(baiduwp_address,baiduwp_passwd,hosts_dir_name,\
 zipfile_passwd,hostsfile_update_date,\
 hostsfile_update_version) =('','','','','',0)

(origin_hostsfile_update_date,origin_hostsfile_update_version)=('',0)
def main():
   (origin_hostsfile_update_date,origin_hostsfile_update_version)=\
     get_hosts_info_from_config_file()

    if is_google_connect.is_google_connected()==False:
        if is_goole_connect.is_network_connected()==True:
            #看来是hosts文件需要更新了
            
            (baiduwp_address,baiduwp_passwd,hosts_dir_name,\
             zipfile_passwd,hostsfile_update_date,\
             hostsfile_update_version)=\
             get_hosts_file_info.get_remote_hosts_file_info(privateutil.get_hosts_url)

            if baiduwp_address!='':
                #获取成功
                if int(hostsfile_update_date)>int(origin_hostsfile_update_date) or\
                   int(hostsfile_update_version)>int(origin_hostsfile_update_version):
                    #需要下载新的文件
                    result_down_zip=download_hosts_zip_file.download_hosts_zip_file(baiduwp_address,baiduwp_passwd,None)
                    if result_down_zip==True:
                        #下载成功
                        zipped_hosts_filename=privateutil.get_the_zipped_hosts_filename()
                        result_unzip=unzip_hosts_zip_file.unzip_zipped_hosts_file(zipped_hosts_filename,zipfile_passwd)
                        if result_unzip==True:
                            #解压缩成功
                            result_update_hosts=update_origin_hosts_file()
                            if result_update_hosts==True:
                                #更新文件成功
                                #更新配置文件，必须成功
                                update_the_config_file(hostsfile_update_date,hostsfile_update_version)
                                #删除zip文件和hosts文件
                                privateutil.clean_downloads()
                                return True
                            else:
                                #更新文件失败哦
                                raise Update_Hostsfile_Failed
                        else:
                            #解压缩失败
                            raise Unzip_Failed
                        
                    else:
                        #下载失败
                        raise Get_Remote_ZipFile_Failed
                    
                else:
                    #文件没有更新且google无法连通，那么只能等待更新咯
                    raise Please_wait_hosts_update
            else:
                raise Get_RemoteHosts_Fileinfo_Failed
        else:
            #网络链接本身有问题
    else:
        #Google是好的
        print 'Google is OK'





class Update_Hostsfile_Failed(Exception):
    pass

class Unzip_Failed(Exception):
    pass

class Get_Remote_ZipFile_Failed(Exception):
    pass

class Please_wait_hosts_update(Exception):
    pass

class Get_RemoteHosts_Fileinfo_Failed(Exception):
    pass

if __name__=='__main__':
    main()
