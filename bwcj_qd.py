"""
time：2024.2.24
new Env('霸王茶姬签到');
环境变量: 名称：bwcjCookie
捉包小程序 webapi.qmai.cn 域名请求头里面的 Qm-User-Token 值

多账号新建变量或者用 & 分开 
2024.3.18 修复无法签到问题，新增抽奖次数参数
在需要执行积分抽奖的token后面加上#抽奖数(每日上限最大5)，每次需要5积分

如：al3U******#5&Qm-User-Token值#3&Qm-User-Token值

并发变量: bwcj_BF  默认不设置为1
"""
import random
import os
import sys
import platform
import subprocess
import time

from functools import partial
import concurrent.futures

token = os.environ.get("bwcjCookie")
if token is None:
    print(f'⛔️未获取到ck：请检查变量是否填写 变量名：bwcjCookie')
    exit(0)

if '&' in token:
    tokens = token.split('&')
else:
    tokens = [token]

bf = os.environ.get("bwcj_BF")
if bf is None:
    print(f'🈳️未设置并发变量，默认1')
    bf = 1

print(f'✅获取到{len(tokens)}个账号 当前设置并发数: {bf}')

file_url = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/Code-KKK/pycode/main/compiled/'

def check_environment(file_name):
    v, o, a = sys.version_info, platform.system(), platform.machine()
    print(f"Python版本: {v.major}.{v.minor}.{v.micro}, 操作系统类型: {o}, 处理器架构: {a}")
    if (v.minor in [8,9,10,11]) and o.lower() in ['linux'] and a.lower() in ['x86_64','aarch64']:
        print("当前环境符合运行要求")
        if o.lower() == 'linux':
            file_name += '.so'
            main_run(file_name, v.minor, o.lower(), a.lower())
    else:
        if not (v.minor in [8,9,10,11]):
            print("不符合运行要求: Python版本不是 3.8 ~ 3.11")
        if not (o.lower() in ['linux']):
            print(f"不符合运行要求: 操作系统类型[{o}] 支持：Linux")
        if not (a.lower() in ['x86_64','aarch64']):
            print(f"不符合运行要求: 当前处理器架构[{a}] 支持：x86_64 aarch64")

def main_run(file_name, py_v, os_info, cpu_info):
    if os.path.exists(file_name):
        file_name_ = os.path.splitext(file_name)[0]
        try:
            Code_module = __import__(file_name_)
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(bf)) as executor:
                for num in range(len(tokens)):
                    runzh = num + 1
                    run = Code_module.bwcj(tokens[num],runzh)
                    executor.submit(run.main)
                    time.sleep(random.randint(2, 5))
        except Exception as e:
            print(str(e)) #打印运行报错信息
            if 'ld-linux-aarch64.so' in str(e):
                print('检测当前系统环境缺失ld-linux-aarch64.so.1请在库里lib目录下载修复ld-linux-aarch64.so.1.sh运行')
    else:
        print(f"不存在{file_name}功能模块,准备下载模块文件")
        download_file(file_name, py_v, os_info, cpu_info,file_url)

def download_file(file_name, py_v, os_info, cpu_info, url):
    file_name_ = os.path.splitext(file_name)[0]
    if os_info == 'linux':
        url = url + f'{file_name_}/{file_name_}.cp3{py_v}-{cpu_info}-{os_info}.so'
    if os_info == 'windows':
        url = url + f'{file_name_}/{file_name_}.cp3{py_v}-win_{cpu_info}.pyd'
    try:
        print(url)
        result = subprocess.run(['curl', '-I', '-s', '-o', '/dev/null', '-w', '%{http_code}', url], capture_output=True, text=True)
        if result.stdout.strip() == '404':
            print('服务器文件不存在,已停止下载')
        else:
            print('服务器文件存在，将开始下载')
            subprocess.run(["curl",'-#',"-o", file_name, url], check=True)
            print(f"{file_name}文件下载成功~开始执行~")
            check_environment(file_name_)
    except subprocess.CalledProcessError:
        print("下载失败，请检查 URL 或 网络问题。")

if __name__ == '__main__':
    print = partial(print, flush=True)
    check_environment("bwcj")
    print('【霸王茶姬·签到】运行完成！🎉')
    