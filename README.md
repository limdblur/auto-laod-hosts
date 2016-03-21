# auto-laod-hosts
自动的更新laod.cn提供的hosts


1 需要安装的软件

  python 2.7 [from official site]
  
    sudo -H pip install bs4 requests
  
  git, wget, Pillow module installation:
  
  MAC OSX
  
  homebrew for mac
  
    brew install wget libjpeg git
    
    sudo -H pip install pillow
  
  Ubuntu
  
  sudo apt-get install python-PIL python-pil python-imaging python-pil.imagetk wget git
  
2 下载&&运行
  
  git clone https://github.com/yanjinyi1987/auto-laod-hosts.git
  
  注意：下载后run.sh中的密码需要修改的，还有存放代码的路径也需要修改
  
  ./run.sh #可能会有窗口弹出要求输入验证码
  
3 致谢

  感谢Github项目 pan-baidu-download
  
    pan-baidu-download: https://github.com/banbanchs/pan-baidu-download.git
    
  感谢我的wife，一个电脑小白
