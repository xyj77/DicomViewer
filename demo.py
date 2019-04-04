# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 15:18:08 2018

@author: rain
"""

import os
import re
import xlwt
import numpy as np
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
import warnings
warnings.filterwarnings("ignore")

#np.set_printoptions(threshold=np.inf)
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory

from dignosis import loadFile, predict, predict2, predict3, predict3d

smallflag=0#判断前几个文件如1是不是要补两个0 001
m5=np.matrix([])
first_x=0
first_y=0
second_x=0
second_y=0
final_x=0
final_y=0
dragflag=0#是否拖动
flag=0#first time?
flag1=0#是否在范围内

temp_x=0
temp_y=0
matrix=np.matrix([])
existflag=0
num_list=[]
save_filename=''
m10=np.array([])
m11=np.array([])
m12=np.array([])
m13=np.array([])
m14=np.array([])

save_x1=0
save_y1=0
save_x2=0
save_y2=0
save_z1=0
save_z2=0

root=tk.Tk() #Toplevel()
i=int()
var = tk.StringVar()
var.set(str(i))


big=0
small=0
filename=''
path=''
timeflag=0
d=""
e=""
filetype ='.dcm'
dicom=str()
dicom1=str()


#config = tf.ConfigProto()
#config.gpu_options.allow_growth = True
#session = tf.Session(config=config)

def first(event):
    global first_x,first_y,flag,flag1,temp_x,temp_y
    if(flag==0):         
        first_x=event.x
        first_y=event.y
    if(flag==1):
        if(((event.x-first_x)*(event.x-second_x))<0 and ((event.y-first_y)*(event.y-second_y))<0):
            flag1=1          
            temp_x=event.x
            temp_y=event.y
            
        
def second(event):
    global second_x,second_y,l,first_x,first_y,rect,dragflag,flag,temp_x,temp_y,flag1
    if (flag==0):  
        dragflag=1
        l.delete(rect)
        second_x=event.x
        second_y=event.y
        rect=l.create_rectangle(first_x, first_y, second_x, second_y,outline='green')
    if(flag==1 and flag1==1):
        if(first_x<second_x and first_y<second_y):
            if(first_x+event.x-temp_x>=0 and first_y+event.y-temp_y>=0 and second_x+event.x-temp_x<=512 and second_y+event.y-temp_y<=512):
                l.delete(rect)
                dragflag=1
                rect=l.create_rectangle(first_x+event.x-temp_x, first_y+event.y-temp_y, second_x+event.x-temp_x, second_y+event.y-temp_y,outline='red')
        if(first_x>second_x and first_y<second_y):
            if(first_x+event.x-temp_x<=512 and first_y+event.y-temp_y>=0 and second_x+event.x-temp_x>=0 and second_y+event.y-temp_y<=512):
                l.delete(rect)
                dragflag=1
                rect=l.create_rectangle(first_x+event.x-temp_x, first_y+event.y-temp_y, second_x+event.x-temp_x, second_y+event.y-temp_y,outline='red')
        if(first_x>second_x and first_y>second_y):
            if(first_x+event.x-temp_x<=512 and first_y+event.y-temp_y<=512 and second_x+event.x-temp_x>=0 and second_y+event.y-temp_y>=0):
                l.delete(rect)
                dragflag=1
                rect=l.create_rectangle(first_x+event.x-temp_x, first_y+event.y-temp_y, second_x+event.x-temp_x, second_y+event.y-temp_y,outline='red')
        if(first_x<second_x and first_y>second_y):
            if(first_x+event.x-temp_x>=0 and first_y+event.y-temp_y<=512 and second_x+event.x-temp_x<=512 and second_y+event.y-temp_y>=0):
                l.delete(rect)
                dragflag=1
                rect=l.create_rectangle(first_x+event.x-temp_x, first_y+event.y-temp_y, second_x+event.x-temp_x, second_y+event.y-temp_y,outline='red')


def final(event):
    global dragflag,flag,rect,second_x,second_y,l,first_x,first_y,temp_x,temp_y,flag1,existflag
    existflag=1
    if (flag==0):       
        if (dragflag==1):  
            l.delete(rect)
            second_x=event.x
            second_y=event.y
            rect=l.create_rectangle(first_x, first_y, second_x, second_y,outline='green')
        dragflag=0
        flag=1;
    if(flag==1 and flag1==1 and dragflag==1):
        first_x=first_x+event.x-temp_x
        first_y=first_y+event.y-temp_y
        second_x=second_x+event.x-temp_x
        second_y=second_y+event.y-temp_y
        l.delete(rect)
        rect=l.create_rectangle(first_x, first_y, second_x, second_y,outline='green')
        temp_x=0
        temp_y=0
        dragflag=0
        flag1=0

            
            
def haress(wc1,ww1,a):
    wc=(wc1/4096)*255
    ww=(ww1/4096)*255
    min = (2*wc - ww)/2.0 + 0.5
    max = (2*wc + ww)/2.0 + 0.5
    dFactor = 255.0/(max - min); 
    a[a<min]=0
    a[a>max]=255
    a = (a - min)*dFactor
    a[a<0]=0
    a[a>255]=255
    return a 
   
    

wc1=tk.IntVar()
wc1.set(1585)
ww1=tk.IntVar()
ww1.set(1585)
def show():
    global filename
    img_array=loadFile(filename)
    a = np.matrix(img_array)
    a=haress(s2.get(),s3.get(),a)
    im=Image.fromarray(a)
    tkimg=ImageTk.PhotoImage(im)
    return tkimg

def processWheel(event):
    global im,filename,var,dicom,second_x,second_y,l,first_x,first_y,rect,big,d,e,i,timeflag,small,smallflag
    if(timeflag==1):
        if (event.delta > 0 and i<big):
            i=i+1
            if(i==0):
                i=1
            if(i==(big+1)):
                i=1
            if(i<10 and small==1 and smallflag==0):
                f=d+'_'+"0"+str((i+small-1))+e
            elif(i<10 and small==1 and smallflag==1):
                f=d+'_'+"00"+str((i+small-1))+e
            elif((i+small-1)<100 and  small==1 and smallflag==1):
                f=d+'_'+"0"+str((i+small-1))+e
            elif((i+small-1)<100 and small>1):
                f=d+'_'+"0"+str((i+small-1))+e
            else:
                f=d+'_'+str((i+small-1))+e
            filename=path+"\\\\"+f
            im=show()
            l.delete(dicom)
            dicom=l.create_image(256,256,image = im)
            var.set(str(i))
            l.create_text(50,10,text = var.get()+'/'+str(big),  fill = 'white')
        
            l.delete(rect)
            rect=l.create_rectangle(first_x, first_y, second_x, second_y,outline='green') 
        elif(event.delta < 0 and i>1):
            i=(i-1)%big
            if(i==0):
                i=big
            if(i<10 and small==1 and smallflag==0):
                f=d+'_'+"0"+str((i+small-1))+e
            elif(i<10 and small==1 and smallflag==1):
                f=d+'_'+"00"+str((i+small-1))+e
            elif((i+small-1)<100 and  small==1 and smallflag==1):
                f=d+'_'+"0"+str((i+small-1))+e
            elif((i+small-1)<100 and small>1):
                f=d+'_'+"0"+str((i+small-1))+e
            else:
                f=d+'_'+str((i+small-1))+e
            filename=path+"\\\\"+f
            im=show()
            l.delete(dicom)
            dicom=l.create_image(256,256,image = im)
            var.set(str(i))
            l.create_text(50,10,text = var.get()+'/'+str(big),  fill = 'white')      
            l.delete(rect)
            rect=l.create_rectangle(first_x, first_y, second_x, second_y,outline='green')
        
        
def change(event):
    global im,l,dicom,second_x,second_y,l,first_x,first_y,rect,timeflag,var,i
    if(timeflag==1):
        im=show()
        l.delete(dicom)
        dicom=l.create_image(256,256,image = im)
        var.set(str(i))
        l.create_text(50,10,text = var.get()+'/'+str(big),  fill = 'white')  
        l.delete(rect)
        rect=l.create_rectangle(first_x, first_y, second_x, second_y,outline='green')

def delete():
    global l,second_x,second_y,l,first_x,first_y,rect,dragflag,flag,flag1,temp_x,temp_y,existflag
    first_x=0
    first_y=0
    second_x=0
    second_y=0
    temp_x=0
    temp_y=0
    flag=0
    flag1=0
    dragflag=0
    l.delete(rect)
    existflag=0
    
def cut():
    global existflag,second_x,second_y,l,first_x,first_y,filename,i,l1,dragflag,flag,flag1,temp_x,temp_y,root,dicom1
    if(existflag==1):
        img_array=loadFile(filename)
        a = np.matrix(img_array)
        #a=haress(s2.get(),s3.get(),a)
        if(first_x<second_x and first_y<second_y):
            b=a[first_y:second_y,first_x:second_x]
        if(second_x<first_x and first_y<second_y):
            b=a[first_y:second_y,second_x:first_x]
        if(second_x<first_x and second_y<first_y):
            b=a[second_y:first_y,second_x:first_x]
        if(first_x<second_x and second_y<first_y):
            b=a[second_y:first_y,first_x:second_x]
        im=Image.fromarray(b)
        tkimg=ImageTk.PhotoImage(im)
        l1.delete(dicom1)
        dicom1=l1.create_image(256,256,image = tkimg)
        root.mainloop()
def save1():
    global save_z1,i,save_z2
    if(save_z1==i):
        tk.messagebox.showinfo('提示', '不要重复保存')
    else:
        save_z1=i
    if(save_z1==save_z2):
        tk.messagebox.showinfo('提示', '两个位置重复')
def save2():
    global save_z1,i,save_z2
    if(save_z2==i):
        tk.messagebox.showinfo('提示', '不要重复保存')
    else:
        save_z2=i
    if(save_z1==save_z2):
        tk.messagebox.showinfo('提示', '两个位置重复')
def save3():
    global save_x1,save_y1,save_x2,save_y2,second_x,second_y,l,first_x,first_y,flag,save_filename,filename
    if(flag==0):
        tk.messagebox.showinfo('提示', '未选取范围')
    else:
        save_x1=first_x
        save_y1=first_y
        save_x2=second_x
        save_y2=second_y
        save_filename=filename
        
DATA=[('路径','z1','z2','x1','y1','x2','y2','分化')
   ]
def settle():
    global save_x1,save_y1,save_x2,save_y2,save_filename,save_z1,save_z2,i,DATA,loop_text
    workbook=xlwt.Workbook(encoding='utf-8')
    booksheet=workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)

    DATA.append((save_filename,save_z1,save_z2,save_x1,save_y1,save_x2,save_y2,loop_text.get()))
    DATA1=tuple(DATA)
    for i,row in enumerate(DATA1):
        for j,col in enumerate(row):
            booksheet.write(i,j,col)
            workbook.save('grade.xls')
    save_z1=0
    save_z2=0
    
def get_filename(path,filetype):
    name =[]
    final_name = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if filetype in i:
                name.append(i.replace(filetype,''))
    final_name = [item +'.dcm' for item in name]
    return final_name


def get():
    global path,filetype,filename,big,d,e,i,timeflag,l,root,dicom,var,small,smallflag
    
    path=askdirectory()
    path=path.replace("/","\\\\")
    a=get_filename(path,filetype)
    b=a.pop()#替换末班
    
    c=a.pop(0)
    rule_name = r'_(\d+).d'
    compile_name = re.compile(rule_name, re.M)
    res_name = compile_name.findall(c)
    if(res_name[0]=='001' or res_name[0]=='002' or res_name[0]=='003' or res_name[0]=='004' or res_name[0]=='005' or res_name[0]=='006' or res_name[0]=='007' or res_name[0]=='008' or res_name[0]=='009'):
        smallflag=1
    else:
        smallflag=0
    small=int(res_name[0])
    
    
    rule_name = r'_(\d+).d'
    compile_name = re.compile(rule_name, re.M)
    res_name = compile_name.findall(b)


    big = int(res_name[0])-small+1
    
    
    rule_name = r'^(.*)_'
    compile_name = re.compile(rule_name, re.M)
    res_name1 = compile_name.findall(b)

    d=res_name1[0]
    e=b[-4:]
    
    if(smallflag==0):
        f=d+'_'+str((big+small-1))+e
        filename=path+"\\\\"+f
    else:
        f=d+'_'+'0'+str((big+small-1))+e
        filename=path+"\\\\"+f
    
    i=big
    im=show()
    timeflag=1
    l.delete(dicom)
    dicom=l.create_image(256,256,image = im)
    var.set(str(i))
    l.create_text(50,10,text = var.get()+'/'+str(big),  fill = 'white')  
    root.mainloop()



def showtest(findlist):
    global second_x,second_y,first_x,first_y,l1,dicom1,root
    b=np.matrix([])
    img_array=loadFile(findlist[0])
    a=np.matrix(img_array)
    if(first_x<second_x and first_y<second_y):
        b=a[first_y:second_y,first_x:second_x]
    if(second_x<first_x and first_y<second_y):
        b=a[first_y:second_y,second_x:first_x]
    if(second_x<first_x and second_y<first_y):
        b=a[second_y:first_y,second_x:first_x]
    if(first_x<second_x and second_y<first_y):
        b=a[second_y:first_y,first_x:second_x]
    ff=np.matrix(b)
#    fffffff1=ff.resize((32, 32))
    
    im1=Image.fromarray(ff)
    img = im1.resize((32,32))
    fff1=np.asarray(img)
    
    
    im=Image.fromarray(fff1)
    tkimg=ImageTk.PhotoImage(im)
    l1.delete("all")
    l1.create_image(256,256,image =tkimg)
    root.mainloop()


    
def curb():
    global existflag,second_x,second_y,l,first_x,first_y,filename,i,big,d,e,matrix,i,small,path
    save3();
    maxqueue=[]
    minqueue=[]
    fff=np.matrix([])
    img_array=loadFile(filename)#得到原始图像
    a = np.matrix(img_array)

    if(first_x<second_x and first_y<second_y):
        b1=a[first_y:second_y,first_x:second_x]
    if(second_x<first_x and first_y<second_y):
        b1=a[first_y:second_y,second_x:first_x]
    if(second_x<first_x and second_y<first_y):
        b1=a[second_y:first_y,second_x:first_x]
    if(first_x<second_x and second_y<first_y):
        b1=a[second_y:first_y,first_x:second_x]
    
    
    for i2 in range(1,big+1):
        if(i2<10 and small==1 and smallflag==0):
            f=d+'_'+"0"+str((i2+small-1))+e
        elif(i2<10 and small==1 and smallflag==1):
            f=d+'_'+"00"+str((i2+small-1))+e
        elif((i2+small-1)<100 and  small==1 and smallflag==1):
            f=d+'_'+"0"+str((i2+small-1))+e
        elif((i2+small-1)<100 and small>1):
            f=d+'_'+"0"+str((i2+small-1))+e
        else:
            f=d+'_'+str((i2+small-1))+e
        filename1=path+"\\\\"+f
        img_array=loadFile(filename1)
        a = np.matrix(img_array)
        #a=haress(s2.get(),s3.get(),a)
        if(first_x<second_x and first_y<second_y):
            b=a[first_y:second_y,first_x:second_x]
        if(second_x<first_x and first_y<second_y):
            b=a[first_y:second_y,second_x:first_x]
        if(second_x<first_x and second_y<first_y):
            b=a[second_y:first_y,second_x:first_x]
        if(first_x<second_x and second_y<first_y):
            b=a[second_y:first_y,first_x:second_x]
        maxqueue.append(b.max())
        minqueue.append(b.min())
        
#        print(b.max())
#        print(b.min())
#    print ("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    #print(max(maxqueue))
    #print(min(minqueue))
    maxValue=max(maxqueue)-100
    minValue=min(minqueue)
    ff=np.array(b1)
    fff=(ff-minValue)/(maxValue-minValue)
    #print(fff)
    
    im1=Image.fromarray(fff)
    img = im1.resize((32,32))
    fff=np.asarray(img)   
    
    
    matrix = fff 
    predict()

#def curb():
#    global existflag,second_x,second_y,l,first_x,first_y,filename,big,d,e,matrix
#    save3();
#    maxqueue=[]
#    minqueue=[]
#    for i in range(1,big):
#        if(i<10):
#            f=d+"0"+str((i))+e
#        else:
#            f=d+str((i))+e
#        filename1=path+"\\\\"+f
#        img_array=loadFile(filename1)
#        a = np.matrix(img_array)
#        #a=haress(s2.get(),s3.get(),a)
#        if(first_x<second_x and first_y<second_y):
#            b=a[first_y:second_y,first_x:second_x]
#        if(second_x<first_x and first_y<second_y):
#            b=a[first_y:second_y,second_x:first_x]
#        if(second_x<first_x and second_y<first_y):
#            b=a[second_y:first_y,second_x:first_x]
#        if(first_x<second_x and second_y<first_y):
#            b=a[second_y:first_y,first_x:second_x]
#        maxqueue.append(b.max())
#        minqueue.append(b.min())
#        
#    print ("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
#    #print(max(maxqueue))
#    #print(min(minqueue))
#    maxValue=max(maxqueue)-500
#    minValue=min(minqueue)
#    ff=np.array(b)
#    fff=(ff-minValue)/(maxValue-minValue)
#    #print(fff)
#    im=Image.fromarray(fff)
#    img = im.resize((32, 32))
#    print ("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
#    matrix = np.asarray(img) 
#    print(matrix)
    
def curb1():
    global existflag,second_x,second_y,l,first_x,first_y,filename,i,big,d,e,m5,small,path
    save3();
    matrix1=[]
    maxqueue=[]
    minqueue=[]
    for i1 in range(1,big+1):
        if(i1<10 and small==1 and smallflag==0):
            f=d+'_'+"0"+str((i1+small-1))+e
        elif(i1<10 and small==1 and smallflag==1):
            f=d+'_'+"00"+str((i1+small-1))+e
        elif((i1+small-1)<100 and  small==1 and smallflag==1):
            f=d+'_'+"0"+str((i1+small-1))+e
        elif((i1+small-1)<100 and small>1):
            f=d+'_'+"0"+str((i1+small-1))+e
        else:
            f=d+'_'+str((i1+small-1))+e
        filename1=path+"\\\\"+f
        img_array=loadFile(filename1)
        a = np.matrix(img_array)
        #a=haress(s2.get(),s3.get(),a)
        if(first_x<second_x and first_y<second_y):
            b=a[first_y:second_y,first_x:second_x]
        if(second_x<first_x and first_y<second_y):
            b=a[first_y:second_y,second_x:first_x]
        if(second_x<first_x and second_y<first_y):
            b=a[second_y:first_y,second_x:first_x]
        if(first_x<second_x and second_y<first_y):
            b=a[second_y:first_y,first_x:second_x]
        maxqueue.append(b.max())
        minqueue.append(b.min())
    if(i>=2 and i<=(big-2)):
        for i2 in range(i-2,i+3):
            if(i2<10 and small==1 and smallflag==0):
                f=d+'_'+"0"+str((i2+small-1))+e
            elif(i2<10 and small==1 and smallflag==1):
                f=d+'_'+"00"+str((i2+small-1))+e
            elif((i2+small-1)<100 and  small==1 and smallflag==1):
                f=d+'_'+"0"+str((i2+small-1))+e
            elif((i2+small-1)<100 and small>1):
                f=d+'_'+"0"+str((i2+small-1))+e
            else:
                f=d+'_'+str((i2+small-1))+e
            filename1=path+"\\\\"+f
            img_array=loadFile(filename1)
            a = np.matrix(img_array)
            #a=haress(s2.get(),s3.get(),a)
            if(first_x<second_x and first_y<second_y):
                b=a[first_y:second_y,first_x:second_x]
            if(second_x<first_x and first_y<second_y):
                b=a[first_y:second_y,second_x:first_x]
            if(second_x<first_x and second_y<first_y):
                b=a[second_y:first_y,second_x:first_x]
            if(first_x<second_x and second_y<first_y):
                b=a[second_y:first_y,first_x:second_x]
            matrix1.append(b)

    #print(max(maxqueue))
    #print(min(minqueue))
    maxValue=max(maxqueue)-100
    minValue=min(minqueue)
    fff=np.matrix([])
    for ff1 in range(0,len(matrix1)):
        ff=np.array(matrix1[ff1])
        fff=(ff-minValue)/(maxValue-minValue)
#        im=Image.fromarray(fff)
#        img = im.resize((32, 32))    
#        matrix = np.asarray(img)
#        matrix1[ff1]=matrix
        
        im1=Image.fromarray(fff)
        img = im1.resize((32,32))
        fff1=np.asarray(img)
        
        matrix = fff1
        matrix1[ff1]=matrix

    m0=np.matrix([])
    m1=np.matrix([])
    m2=np.matrix([])
    m3=np.matrix([])
    m4=np.matrix([])
    m5=np.matrix([])
    m0=matrix1[0]
    m1=matrix1[1]
    m2=matrix1[2]
    m3=matrix1[3]
    m4=matrix1[4]
    m5=np.dstack((m0,m1))
    m5=np.dstack((m5,m2))
    m5=np.dstack((m5,m3))
    m5=np.dstack((m5,m4))
    predict3d()

            
            
s2 = tk.Scale(root,
      from_ = 10,#设置最小值
      to = 40950,#设置最大值
      orient = tk.HORIZONTAL,#设置横向
      resolution=5,#设置步长
      tickinterval = 5000,#设置刻度
      length = 500,# 设置像素
      variable = ww1,
      command=change)#绑定变
s2.grid(row=1,column=1)

s3 = tk.Scale(root,
      from_ = 20,#设置最小值
      to = 40950,#设置最大值
      resolution=5,#设置步长
      tickinterval = 5000,#设置刻度
      length = 500,# 设置像素
      variable = wc1,
      command=change)#绑定变量
s3.grid(row=0,column=2) 

l = tk.Canvas(root,width = 512, height = 512,bg = 'white')

l.bind("<MouseWheel>", processWheel)

rect=l.create_rectangle(first_x, first_y, second_x, second_y)
l.bind("<Button-1>",first)
l.bind("<B1-Motion>",second)
l.bind("<ButtonRelease-1>",final)
l.grid(row=0,column=1)



b1 = tk.Button(root, text='清除',width=12,command=delete)
b2 = tk.Button(root, text='截取',width=12,command=cut)
b3 = tk.Button(root, text='肿瘤起始坐标',width=12,command=save1)
b4 = tk.Button(root, text='肿瘤终止坐标',width=12,command=save2)
b5 = tk.Button(root, text='肿瘤截面范围',width=12,command=save3)
b6 = tk.Button(root, text='记录',width=12,command=settle)
b7 = tk.Button(root, text='读取',width=12,command=get)
b8 = tk.Button(root, text='2d预测',width=12,command=curb)
b9 = tk.Button(root, text='3d预测',width=12,command=curb1)
b10 = tk.Button(root, text='二分类',width=12,command=predict2)
b11 = tk.Button(root, text='三分类',width=12,command=predict3)

b7.grid(row=0,column=0,sticky='N') 
b1.place(x = 0, y = 40)
b2.place(x = 0, y = 80)
b3.place(x = 0, y = 120)
b4.place(x = 0, y = 160)
b5.place(x = 0, y = 200)
b6.place(x = 0, y = 240)
#b8.place(x = 0, y = 280)
#b9.place(x = 0, y = 320)
b10.place(x = 0, y = 360)
b11.place(x = 0, y = 400)

l3 = tk.Label(root, text="分化程度：")
l3.place(x = 10, y = 280)
loop_text = tk.StringVar()
loop = tk.Entry(root, textvariable = loop_text,width=12)
loop_text.set(" ")
loop.place(x = 5, y = 300)

root.mainloop()