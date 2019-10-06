#-*- coding: utf-8 -*-
from django.views.decorators.cache import cache_page
from django.http import HttpResponse,HttpRequest,JsonResponse
from django.template import RequestContext
from django.shortcuts import render,render_to_response
from django.views.decorators import csrf
import glob
import mimetypes
import smtplib,os,time
from email import encoders
from email.message import Message
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from Protein.models import Profile
from django.contrib import messages
import shlex
from Bio import SeqIO
from Bio.Alphabet import generic_dna
from django.contrib.sessions.models import Session
import logging
import subprocess
from io import StringIO
from Protein.models import Profile
import os
from django.http import HttpResponseRedirect
from .form import UploadFileForm
import random
from django.urls import reverse
from email.mime.multipart import MIMEMultipart
def run_shell_command(command_line):
    command_line_args = shlex.split(command_line)

    logging.info('Subprocess: "' + command_line + '"')

    try:
        command_line_process = subprocess.Popen(
            command_line_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        process_output, _ =  command_line_process.communicate()

        # process_output is now a string, not a file,
        # you may want to do:
        # process_output = StringIO(process_output)
        log_subprocess_output(process_output)
    except (OSError, CalledProcessError) as exception:
        logging.info('Exception occured: ' + str(exception))
        logging.info('Subprocess failed')
        return False
    else:
        # no exception was raised
        logging.info('Subprocess finished')

    return True
def sendmail(user_mail,file_name,user_id):

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
    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = user_mail
# --- Email 的主旨 Subject ---
    msg["Subject"] = "Protein Prediction Test"
    part = MIMEText("\n Send from NCCU Protein prediction ", _charset="UTF-8")
    msg.attach(part)
    #msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n" % (gmail_user, toaddrs, "Protein prediction"))
    ctype, encoding = mimetypes.guess_type('../predict/Output/'+user_id+"/"+file_name+'/vote_score.txt')
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    fp = open('../predict/Output/'+user_id+"/"+file_name+'/vote_score.txt', "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=file_name+".txt")
    msg.attach(attachment)

    #smtpserver.sendmail(fromaddr, toaddrs, msg+info)
    #server = smtplib.SMTP('smtp.gmail.com', 587)
    #server.ehlo()
    #server.starttls()
    # --- 如果SMTP server 不需要登入則可把 server.login 用 # mark 掉
    #server.login(username,password)
    smtpserver.sendmail(fromaddr, toaddrs, msg.as_string())
    smtpserver.quit()
#記得要登出
   # smtpserver.quit()
def is_fasta(filename):
    """with open (filename,'r') as handle:
        fasta = SeqIO.parse(handle,"fasta")
	print("fasta:")
	print(handle.read())
        return any(fasta)"""
    for record in SeqIO.parse(filename,"fasta",generic_dna):
        return any(record)

def search_post(request):
    if 'visited' in request.session:
        if request.session['visited']==True:
            url="result?id="+request.session['id']
            return HttpResponseRedirect(url)
    if 'user_id' not in request.session:
        request.session['user_id']=str(random.randint(0,100000))
        command="mkdir ../predict/Output/"+request.session['user_id']
        os.system(command)
        command="mkdir ../predict/Upload/"+request.session['user_id']
        os.system(command)

    return render(request, "post.html")


def goto_searchpost(request):
    del request.session['visited']
    del request.session['email']
    del request.session['comment']
    return HttpResponseRedirect('psldoc3')
def download_file(request):
    # do something
    time.sleep(1)
    print(type(request.GET['id']))
    filename="../predict/Output/"+request.session['user_id']+"/"+request.GET['id']+"/vote_score.txt"
    with open(filename) as f:
        c = f.read()
    return HttpResponse(c)
def upload_file(request):
    print(type(request.GET['id']))
    filename="../predict/Upload/"+request.session['user_id']+"/"+request.GET['id']+".fasta"
    with open(filename) as f:
        c = f.read()
    return HttpResponse(c)
def history(request):
    #userlist=[]
    #files1 = glob.glob('../predict/Output/'+request.session['user_id']+'/*')
    #files2 = glob.glob('../predict/Upload/'+request.session['user_id']+'/*')
    #print(files1)
    #print(files2)

    #for (f1,f2) in zip(files1,files2):
    #    tmp={'time':1200,'user_id':request.session['user_id'],'upload_file':f1,'result_file':f2 }
    #    userlist.append(tmp)
    if 'user_id' in request.session:
        i = Profile.objects.filter(user_name=request.session['user_id'])
    return render_to_response('history.html',locals())

def result(request):
    if 'visited' in request.session:
        filename="../predict/Output/"+request.session['user_id']+"/"+request.GET['id']+"/vote_score.txt"
        with open(filename) as f:
            c = f.read()

        data=c
        return render_to_response('result.html',locals())

    else:
        error=False
        comment=request.POST['comment']
        email = request.POST['email']
        request.session['email']=email
        request.session['comment']=comment
        if 'sessionid' in request.COOKIES:
            print("yes in session")
        #sid=request.COOKIES['sessionid']
        #print(sid)
        #sid = request.session.session_key
        #print(sid)

        request.session['id']=request.GET['id']
	#print("session: "+sid)
        #file_name="xxxx"
        testfile= request.POST.get('input_file',False)
        request.session['input_file']=testfile
        #@form = UploadFileForm(request.POST, request.FILES)
        #print request.POST
        #if form.is_valid():
        #    print "valid"
        #    handle_uploaded_file(request.FILES['input_file'])

        print ("comment: "+comment)
        print (testfile)
        files = [f for key, f in request.FILES.items()]
        print(files)
        if(( len(files)==0) and ( not comment )):
            error=True
            print ("both are None")
        else:
            if  not comment  :
                print("is file")
                filename = request.GET['id']+".fasta"
                file_path="../predict/Upload/"+request.session['user_id']+"/"+filename
                handle_uploaded_file(files[0],file_path)
            else:
                print("is comment")
                filename = request.GET['id']+".fasta"
                file_path="../predict/Upload/"+request.session['user_id']+"/"+filename
                with open(file_path, 'wb+') as destination:
                    destination.write(comment)
                destination.close()
            if is_fasta(file_path):
                error=False
                print("error = false")
            else:
                error=True
                print("error = true")

    #error = True
        if error==True:
            request.session['error']=error
            messages.warning(request,"Please correct the error below")
            return HttpResponseRedirect('psldoc3')
        reloads=1
        return render_to_response('result.html',locals())
# Create your views here.
def load_file(request):
    if 'visited' in request.session:
        res=0
        return JsonResponse(res,safe=False)
    comment=request.session['comment']
    if not comment :
        filename = request.session['id']+".fasta"
        file_path="../predict/Upload/"+request.session['user_id']+'/'+filename
        #handle_uploaded_file(files[0],file_path)
        path="../predict/"
        os.chdir(path)
        command="nextflow predict.nf --query Upload/"+request.session['user_id']+"/"+filename+" --output Output/"+request.session['user_id']+'/'+request.session['id']
        os.system(command)
    else:
        print( "no in file")
        filename=request.session['id']+".fasta"
        #fn=open(filename,"wb+")
        #fn.writelines(data)
        #fn.close()
        path="../predict/"
        os.chdir(path)
        command="nextflow predict.nf --query "+"Upload/"+request.session['user_id']+"/"+filename+" --output Output/"+request.session['user_id']+"/"+request.session['id']
        os.system(command)

    #file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    p=Profile(user_name=request.session['user_id'],email=request.session['email'],comment=request.session['id'])
    p.save()
        #data=request.POST['comment']
    filename="../predict/Output/"+request.session["user_id"]+"/"+request.session['id']+"/vote_score.txt"
    with open(filename) as f:
        c = f.read()
    data=c

    sendmail(request.session['email'],request.session['id'],request.session['user_id'])
    request.session['visited']=True
    res=0
    reloads=0
    return JsonResponse(res,safe=False)
def handle_uploaded_file(f,f_path):
    with open(f_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
