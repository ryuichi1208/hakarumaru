import os
import json
import psycopg2

from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, AudioMessage


app = Flask(__name__)

user_id = "Ueb00df84c77cf0167b07fe0682eb709c"
YOUR_CHANNEL_SECRET = "610989f0eb3dd983010087a2bbc4b7ea"
YOUR_CHANNEL_ACCESS_TOKEN = "YNvQUWGAzSTIIMzyPgkBIaktnNZQgR4YkvUBZGFQIjWcSAFu8acgj94ePqeJGCN1isSyyc0QKCbYEx2gN50TLf+ordWojC+XT4gZyyXSWVxoObh9WSiioLbpgg6JWyxyLYgJXXQ8rEXacb3hpOXW0AdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

def is_authorize(user, password):
    if user in ["root", "metric"] and password is "password":
        return True
    else:
        return False


@app.route("/api/db/test", methods=['GET'])
def db_test():
    dsn = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute('SELECT * FROM dzed')
    res = {}
    for i in cur:
        res[i[0]] : i[1]

    print(res)
    return jsonify(res)


@app.route("/update", methods=['POST'])
def update_host_info():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    filepath = f'{data["host"]}.txt'

    host_info = {
        "hostname": data["host"],
        "kernel": data["kernel"],
        "mem": data["mem"],
        "instruction": data["instruction"]
    }

    with open(filepath, mode='w') as f:
        js = json.dumps(host_info)
        json.dump(js, f, ensure_ascii=False)

    with open(filepath) as f:
        return json.load(f)


@app.route("/cpu", methods=['POST'])
def return_ok():
    data = request.data.decode('utf-8')
    data = json.loads(data)

    try:
        if is_authorize(str(data["user"]), str(data["pass"])) == 0:
            pass
        else:
            return "NG"
    except KeyError:
        return "NG"

    img_url = str(data['key'])
    messages = TextSendMessage(text=img_url)
    line_bot_api.push_message(user_id, messages=messages)
    return 'OK'


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


def get_host_info(host):
    filepath = f'{host}.txt'

    try:
        with open(filepath) as f:
            js = json.load(f)
            js = json.loads(js)
    except FileNotFoundError:
        return "そんなサーバないよ😡 : " + host

    return f'ホスト名：{js["hostname"]}\nkernel : {js["kernel"]}\nmem: {js["mem"]}'

def dispatch_response(msg):
    status = {
        100: "Continue",
        101: "Switching Protocol",
        103: "Early Hints",
        200: "OK",
        203: "Non-Authoritative Information",
        300: "Multiple Choice",
        305: "Use Proxy : プロキシを使用せよ。",
        403: "Forbidden",
        404: "Not found",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict : 競合。要求は現在のリソースと競合するので完了出来ない。",
        414: "URI Too Long",
        451: "Unavailable For Legal Reasons",
        500: "Internal Server Error : サーバ内部エラー",
        503: "Service Unavailable : サービス利用不可",
        510: "Not Extended",
        511: "Network Authentication Required"
    }

    errno = {
        1: "EPERM: Operation not permitted",
        2: "ENOENT: No such file or directory",
        5: "EIO: I/O error",
        110: "ETIMEDOUT: Connection timed out",
        114: "EALREADY: Operation already in progress"
    }

    signal = {
        2: "SIGINT: Term キーボードからの割り込み",
        11: "SIGSEGV: Core 不正なメモリー参照"
    }

    cmd = msg.split()
    if cmd[0] in ["h", "http"]:
        try:
            res = status[int(cmd[1])]
        except KeyError:
            res = "The specified status is undefined"
    elif cmd[0] in ["e", "errno"]:
        try:
            res = errno[int(cmd[1])]
        except KeyError:
            res = "The specified errno is undefined"
    elif cmd[0] in ["s", "signal"]:
        try:
            res = signal[int(cmd[1])]
        except KeyError:
            res = "The specified signal is undefined"
    elif "の情報" in cmd[0]:
        res = get_host_info(cmd[0][0:cmd[0].find("の")])
    else:
        res = msg

    return res


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(dispatch_response(event.message.text))
    )

@handler.add(MessageEvent, message=(ImageMessage, AudioMessage))
def handle_image_audio_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="image")
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
