# encoding:utf-8
import subprocess
from functools import  partial
subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
import execjs

script = ''
with open('./pkulaw.js','r',encoding='utf-8') as file:
    script = file.read()
exec_function = execjs.compile(script,cwd='D:\\个人git\chrome_js\\node_modules')
def encryption(password, encryptionKey):
    return exec_function.call('encryption',password,encryptionKey)


if __name__ == '__main__':
    script = ''
    with open('./pkulaw.js','r',encoding='utf-8') as file:
        script = file.read()
    exec_function = execjs.compile(script,cwd='D:\\个人git\chrome_js\\node_modules')
    print(exec_function.call('encryption','qq123456789','ec43c708a210421ea61410d8efe9a8e2'))
