
#Xencode
import math

def force(msg):
    ret = []
    for w in msg:
        ret.append(ord(w))
    return bytes(ret)
def ordat(msg, idx):
    if len(msg) > idx:
        return ord(msg[idx])
    return 0
def sencode(msg, key):
    l = len(msg)
    pwd = []
    for i in range(0, l, 4):
        pwd.append(
            ordat(msg, i) | ordat(msg, i + 1) << 8 | ordat(msg, i + 2) << 16
            | ordat(msg, i + 3) << 24)
    if key:
        pwd.append(l)
    return pwd
def lencode(msg, key):
    l = len(msg)
    ll = (l - 1) << 2
    if key:
        m = msg[l - 1]
        if m < ll - 3 or m > ll:
            return
        ll = m
    for i in range(0, l):
        msg[i] = chr(msg[i] & 0xff) + chr(msg[i] >> 8 & 0xff) + chr(
            msg[i] >> 16 & 0xff) + chr(msg[i] >> 24 & 0xff)
    if key:
        return "".join(msg)[0:ll]
    return "".join(msg)
def get_xencode(msg, key):
    if msg == "":
        return ""
    pwd = sencode(msg, True)
    pwdk = sencode(key, False)
    if len(pwdk) < 4:   
        pwdk = pwdk + [0] * (4 - len(pwdk))
    n = len(pwd) - 1
    z = pwd[n]
    y = pwd[0]
    c = 0x86014019 | 0x183639A0
    m = 0
    e = 0
    p = 0
    q = math.floor(6 + 52 / (n + 1))
    d = 0
    while 0 < q:
        d = d + c & (0x8CE0D9BF | 0x731F2640)
        e = d >> 2 & 3
        p = 0
        while p < n:
            y = pwd[p + 1]
            m = z >> 5 ^ y << 2
            m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
            m = m + (pwdk[(p & 3) ^ e] ^ z)
            pwd[p] = pwd[p] + m & (0xEFB8D130 | 0x10472ECF)
            z = pwd[p]
            p = p + 1
        y = pwd[0]
        m = z >> 5 ^ y << 2
        m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
        m = m + (pwdk[(p & 3) ^ e] ^ z)
        pwd[n] = pwd[n] + m & (0xBB390742 | 0x44C6F8BD)
        z = pwd[n]
        q = q - 1
    return lencode(pwd, False)
##Xencode

#base64
_PADCHAR = "="
_ALPHA = "LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA"
def _getbyte(s, i):
    x = ord(s[i]);
    if (x > 255):
        print("INVALID_CHARACTER_ERR: DOM Exception 5")
        exit(0)
    return x
def get_base64(s):
    i=0
    b10=0
    x = []
    imax = len(s) - len(s) % 3;
    if len(s) == 0:
        return s
    for i in range(0,imax,3):
        b10 = (_getbyte(s, i) << 16) | (_getbyte(s, i + 1) << 8) | _getbyte(s, i + 2);
        x.append(_ALPHA[(b10 >> 18)]);
        x.append(_ALPHA[((b10 >> 12) & 63)]);
        x.append(_ALPHA[((b10 >> 6) & 63)]);
        x.append(_ALPHA[(b10 & 63)])
    i=imax
    if len(s) - imax ==1:
        b10 = _getbyte(s, i) << 16;
        x.append(_ALPHA[(b10 >> 18)] + _ALPHA[((b10 >> 12) & 63)] + _PADCHAR + _PADCHAR);
    else:
        b10 = (_getbyte(s, i) << 16) | (_getbyte(s, i + 1) << 8);
        x.append(_ALPHA[(b10 >> 18)] + _ALPHA[((b10 >> 12) & 63)] + _ALPHA[((b10 >> 6) & 63)] + _PADCHAR);
    return "".join(x)
#base64

#md5
import hmac
import hashlib
def get_md5(password,token):
	return hmac.new(token.encode(), password.encode(), hashlib.md5).hexdigest()
#md5 

#sha1
import hashlib
def get_sha1(value):
    return hashlib.sha1(value.encode()).hexdigest()
#sha1

import requests
import time
import re
import os

header={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36'
}

init_url="http://10.253.0.100/"
get_challenge_api="http://10.253.0.100/cgi-bin/get_challenge"

srun_portal_api="http://10.253.0.100/cgi-bin/srun_portal"


n="200"
enc="srun_bx1"
type="1"
callback="jQuery11240645308969735664_"+str(int(time.time()*1000))
get_token_param={}
ac_id =""
proxy={
        "http" : "",
        "https" : ""
    }
def get_acid():
    url="http://www.gstatic.com"
    global ac_id
    header={
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }

    init_gstatic=requests.get(url,headers=header,proxies=proxy)
    print("____________________")
    print("init_text="+init_gstatic.text)
    try:
        try:
            ac_id=re.search('id="ac_id" value="(.*?)"',init_gstatic.text).group(1)
        except:
            ac_id=re.search("index_(.*?).html",init_gstatic.text).group(1)
    except:
        print('有可能你已经卡上线了，无需登录，请检查')
        os._exit(0)
        
    #print(init_gstatic.text)
    print("____________________")
    print("ac_id="+ac_id)

    
    
def init_getip():
    global ip,ac_id
    init_res=requests.get(init_url,headers=header,proxies=proxy)
    #print("init_res="+init_res.text)
    print("初始化获取ip")
    ip=re.search('id="user_ip" value="(.*?)"',init_res.text).group(1)
    print("ip:"+ip)
    print("ac_id:"+ac_id)
    print("__________________________________________________")
    #print(init_res.text)
    
    print("__________________________________________________")
#init_getip()


def init_token():
    global get_token_param
    get_token_param={
        "callback" : "jQuery112402876156587315255_"+str(int(time.time()*1000)),
        "username" : username,
        "ip" : ip,
        "_" : int(time.time()*1000),
    }
    print("get_token_param="+str(get_token_param))



def init_print_token():
    global token
    try:
        print("______________________________________")
        init_token=requests.get(get_challenge_api,params=get_token_param,headers=header,proxies=proxy)
        print("token_init="+init_token.text)
        token=re.search('"challenge":"(.*?)"',init_token.text).group(1)
        
        print("token:"+token)
    except (AttributeError):
        print("获取token失败:未匹配到challenge")
        
def hmd5(): 
    global pwmd5, hmd5
    hmd5 = get_md5(password,token)
    pwmd5="{MD5}"+get_md5(password,token)
    
def get_info():
    acid,enc_ver ="",""
    global i
    
    info={
        "username": username,
        "password": password,
        "ip": ip,
        "acid": ac_id,
        "enc_ver": enc
        
    } 
    i = re.sub("'",'"',str(info))
    i = re.sub(" ",'',i)
    print("i="+i)
    i ="{SRBX1}" + get_base64(get_xencode(i,token))
    print("info="+i)

def get_chkstr():
    global pwmd5,chksum

    chkstr = token + username
    chkstr += token + hmd5
    chkstr += token + ac_id
    chkstr += token + ip
    chkstr += token + n
    chkstr += token + type
    chkstr += token + i
    print("_______________________")
    print("chkstr="+chkstr)
    chksum=get_sha1(chkstr)
    print("chksum="+chksum)
    
def login():
    global RES
    srum_login_params={
        "callback": 'jQuery11240645308969735664_'+str(int(time.time()*1000)),
        "action":"login",
        "username":username,
        "password":pwmd5,
        "ac_id":ac_id,
        "ip":ip,
        "chksum":chksum,
        "info":i,
        "n":n,
        "type":type,
        "os":"Windows 10",
        "name":"Windows",
        "double_stack":"0",
        '_':str(int(time.time()*1000))
    }
    print('srum_login_params= '+str(srum_login_params))

    RES=requests.get(srun_portal_api,params=srum_login_params,headers=header,proxies=proxy)     
    print("LOG="+RES.text)
    try: 
        login_status=re.search('"suc_msg":"(.*?)"',RES.text).group(1)
    except:
        print('登录错误，请检查用户名与密码')
    #print(login_status)
    if login_status == 'login_ok':
        print("login success")
    else:
        print("login failed")
       
def logout():
    import socket
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print("ip="+ip)
    
    header={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36'
    }

    url="http://10.253.0.100/cgi-bin/srun_portal"
    params={
        'callback':'jQuery11240645308969735664_'+str(int(time.time()*1000)),
        'action':"logout",
        'acid':'1',#这里acid的值似乎不重要
        'ip':ip,
        'username':username,
        '_':str(int(time.time()*1000))
    }
    print(str(params))
    log_logout=requests.get(url,params=params,headers=header,proxies=proxy)
    print(log_logout.text)
   
    logout_status=re.search('"error_msg":"(.*?)"',log_logout.text).group(1)
    
    #print("logout_status="+logout_status)
    
    if logout_status == "":
        print("Logged out")
    elif logout_status == "You are not online.":
        print("No need to logout")
  
'''  
def detect_online_status():
    url_online="http://10.253.0.100/cgi-bin/rad_user_info"
    online_param={
        "callback":callback,
        "_":str(int(time.time()*1000))
    }
    online_status=str(requests.get(url_online,params=online_param,headers=header))
    #if re.search()
    print(online_status)
'''    
def detecttime():

    inshr = int(time.strftime("%H",time.localtime()))
    if inshr < 8 or inshr >23:
        print("现在未到达可登录时间")
        print("是否继续登录？")
        os.system('pause')

def getidpw():
    
    global username, password
    idpwpath = r'assets/id_pw.txt'
    try:
        with open(idpwpath,'r') as content:
            global username, password
            fileopen = content.read()
            print(fileopen)
            username = re.search('id:(.*)\\n',fileopen).group(1)
            password = re.search('pw:(.*)',fileopen).group(1)
    except FileNotFoundError as e:
        print('erro code= '+ str(e) +'\n请使用本路径下的 ##第一次使用点这里初始化用户名密码.bat## 完成初始化')
        
        os._exit(0)
    #print(username,password)
    
    
    
    
    


username=""
password=""
#username=input("输入用户名")#在此输入用户名 
#password=input("输入密码")#在此输入密码

#detect_online_status()

getidpw()
logout()#if online

get_acid()
init_getip()
init_token()
init_print_token()
hmd5()
get_info()
get_chkstr()
login()
