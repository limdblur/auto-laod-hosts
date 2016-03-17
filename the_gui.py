#!/usr/bin/python
#encoding:utf-8

import Tkinter
from PIL import ImageTk,Image
#上面一句话与PIL.ImageTk有什么区别呢
global_vcode=''
def input_vcode(image_file):
    
    top=Tkinter.Tk()
    frame=Tkinter.Frame(top)
    frame.pack()

    bottomframe=Tkinter.Frame(top)
    bottomframe.pack(side=Tkinter.BOTTOM)

    #open image_file
    #http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/images.html#class-PhotoImage
    #try:
    #    vcode_img_object=Tkinter.PhotoImage(file=image_file) #这货不能load jpg file
    #except Exception,e:
    #    vcode_img_object=None
    #    print e

    #open JPG file
    #http://stackoverflow.com/questions/23901168/how-do-i-insert-a-jpeg-image-into-a-python-tkinter-window
    fp=open(image_file,'rb')
    vcode_image_object=ImageTk.PhotoImage(Image.open(fp))
    fp.close()
    
        
    #var=Tkinter.StringVar() #StringaVar()是Tkinter预定义的
    #label_vcode=Tkinter.Label(top,textvariable=var,relief=Tkinter.RAISED) #Label一般用常量了
    #var.set(u'请输入验证码：')
    label_vcode=Tkinter.Label(frame,text=u'请输入验证码：',relief=Tkinter.FLAT)
    label_vcode.pack(side=Tkinter.LEFT)

    label_vcode_text=Tkinter.Entry(frame,bd=2)
    label_vcode_text.pack(side=Tkinter.LEFT)
    label_vcode_image=Tkinter.Label(frame,image=vcode_image_object,relief=Tkinter.RAISED)
    label_vcode_image.pack(side=Tkinter.LEFT)
    def set_global_vcode():
        global global_vcode
        global_vcode=label_vcode_text.get()
        top.destroy()
        
    ok_button=Tkinter.Button(bottomframe,text=u'OK',command=set_global_vcode) #点击button后设置global_vcode

    ok_button.pack(side=Tkinter.LEFT)

    top.mainloop()
    #return global_vcode


if __name__=='__main__':
    vcode_image_file=u'vcode.jpg'
    input_vcode(vcode_image_file)
    #input_vcode()
    pass
