# -*- coding: utf-8 -*-
from django.http import HttpResponse 
from django.shortcuts import render,render_to_response
from django.views.decorators import csrf
import smtplib,os,time
# 接收POST请求数据
def sendmail(user_mail):
 
    info = ''
    info += ('\n'+"tes123"+'\n')
   # info += ('\n'+u'因資訊安全，請至(http://******.nchu-cm.com/)， 登入後觀看預警內容'+'\n')
 
    gmail_user = 'eric0330eric@gmail.com'
    gmail_pwd = 'ricky42613'
#這是GMAIL的SMTP伺服器，如果你有找到別的可以用的也可以換掉
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
#登入系統
    smtpserver.login(gmail_user, gmail_pwd)
     
#寄件人資訊
    fromaddr = "*************@gmail.com"
#收件人列表，格式為list即可
    toaddrs = user_mail 
#設定寄件資訊
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n" % (gmail_user, toaddrs, "Protein prediction"))
 
    smtpserver.sendmail(fromaddr, toaddrs, msg+info)
 
#記得要登出
    smtpserver.quit()

def search_post(request):

    if 'comment' in request.POST:
        
        print("email: ",request.POST['email'])
        print("name: ",request.POST['user_name'])
        print("comment: ",request.POST['comment'])
        sendmail(request.POST['email'])
        #ctx['rlt'] = request.POST['q']
        #return render(request,"result.html")
    return render(request, "post.html")
    
def download_file(request):  
    # do something
    time.sleep(10)
    print(type(request.GET['id']))
    filename="./Data/"+request.GET['id']+".txt"
    with open(filename) as f:
        c = f.read()
    return HttpResponse(c)
def readFile(filename,chunk_size=512):  
    with open(filename,'rb') as f:  
        while True:  
            c=f.read(chunk_size)  
            if c:  
                yield c  
            else:  
                break  



def result(request):
    #f=request.POST.FILES['testfile']
    """with open('./Upload/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    """
    data=request.POST['comment']
    sendmail(request.POST['email'])    
    filename="./Data/"+request.GET['id']+".txt"
    fn=open(filename,"w+")
    fn.writelines(data)
    fn.close()
    print(request.GET['id'])
    return render_to_response('result.html',locals())
