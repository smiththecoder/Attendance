from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
import requests
from .models import Rollno

import re
import json

# Create your views here.

url="False"

    
def cooki():  
    try:
        q=requests.get("http://login.sreyas.ac.in:80/authcheck.aspx",allow_redirects=False)	
        cook=q.cookies.get_dict()
        q=requests.get("http://login.sreyas.ac.in:80/default.aspx",allow_redirects=False,cookies=cook)
        burp0_data = {"__VIEWSTATE": q.text[1759:2047], "__VIEWSTATEGENERATOR": "CA0B0334", "__EVENTVALIDATION": q.text[2227:2315], "txtId1": '', "txtPwd1": '', "txtId2": "21ve1a6680", "txtPwd2": "webcap", "imgBtn2.x": "40", "imgBtn2.y": "4"}
        q=requests.post("http://login.sreyas.ac.in:80/default.aspx",cookies=cook,data=burp0_data,allow_redirects=False)
        with open("keys.txt","w") as f:
            f.write(cook['ASP.NET_SessionId']+'\n'+q.cookies['frmAuth'])
    except:
        return "retry"

def getAttendance(roll):
    try:
        with open('keys.txt','r') as f:
            key=f.read().split('\n')
        url = "http://login.sreyas.ac.in:80/ajax/StudentAttendance,App_Web_studentattendance.aspx.a2a1b31c.ashx?_method=ShowAttendance&_session=no"
        cookiess = {"ASP.NET_SessionId":key[0], "frmAuth": key[1]}
        data = f"""rollNo={roll}
fromDate=
toDate=
excludeothersubjects=false"""
    
        q=requests.post(url, cookies=cookiess, data=data)
        t=q.content[:9]
        if(t==b'\r\n\r\n<!DOC'):
            cooki()
            return getAttendance(roll)
        else:
            return q.text[980:-318]
    except Exception as e:
        return "retry"

def home(request):
    request.session.flush()
    print(request.session.items())
    if request.session.items():
        return HttpResponse("<h1>multiple times not allowed please try after 24 hours...</h1>")

    if(url=="False"):
        if(request.method=="POST"):
            roll=request.POST.get('rolln')
            js="""
            window.location.href="/result";
            """
            request.session['data']=getAttendance(roll);
            context={'js':js}
            Rollno(roll=roll).save()
            return render(request,"index.html",context)
        return render(request,"index.html")
    else:
        return redirect("https://studentattence-v3ab.onrenderr.com")

def main(request):
    if(request.method=="POST"):
        key=request.POST.get('rolln')
        global url
        context={"data":"unsuccesfull retry"}
        if(key=="stop"):
            url="True"
            context={"data":"Success"}
        elif(key=="start"):
            url="False"
            context={"data":"Success"}
        elif(key=="display"):
            context={"data":list(Rollno.objects.all())}
       
        return render(request,"main.html",context)

    return render(request,"main.html")


def res(request):
    context={"data":request.session.get("data")}
    request.session['data']="False"
    return render(request,"result.html",context)
