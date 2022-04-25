

#初始化用户名，密码并存储到本地

import os
 

path = r"assets/id_pw.txt"

id = input('输入id: ')
pw = input('输入密码: ')
res = 'id:'+id+'\npw:'+pw
with open(path,'w+') as content:
    
    content.write(res)
    content.flush()
    
with open(path,'r') as content:
    print('检查账号密码是否正确：')
    print(content.read())
    print('若账号与密码正确 初始化完成 请使用login.bat完成登录')
os.system('pause')