import os
import sys
import psutil
import requests
import json

def get_cpu():
    return '[%s]' % os.uname()[1], psutil.cpu_percent(interval=1), psutil.virtual_memory().percent


def exec_curl(met):
    user = "root"
    password = "passowrd"
    url = "https://hakarumaru.herokuapp.com/cpu"
    header = "Content-Type: application/json"
    msg = f'ホスト: {met[0]}\nCPU使用率 : {met[1]}%\nメモリ使用率 : {met[2]}% '

    response = requests.post(
        url,
        json.dumps({'user':user, 'pass': password, 'key': msg}),
        headers={'Content-Type': 'application/json'})


def main():
    exec_curl(get_cpu())


if __name__ == "__main__":
    main()
