# encoding:utf-8
import subprocess
from functools import  partial
subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
import execjs

script = ''
with open('./pkulaw.js','r',encoding='utf-8') as file:
    script = file.read()
exec_function = execjs.compile(script,cwd='D:\\个人git\chrome_js\\node_modules')
#北大法宝password加密
def encryption(password, encryptionKey):
    return exec_function.call('encryption',password,encryptionKey)


if __name__ == '__main__':
    script = ''
    with open('./pkulaw.js','r',encoding='utf-8') as file:
        script = file.read()
    exec_function = execjs.compile(script,cwd='D:\\个人git\chrome_js\\node_modules')
    print(exec_function.call('encryption','Cyd0217@','71ee1118adac4321a63f93be1ddf9420'))
