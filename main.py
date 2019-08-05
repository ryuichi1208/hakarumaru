from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

YOUR_CHANNEL_SECRET = ""
YOUR_CHANNEL_ACCESS_TOKEN = ""

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def return_ok():
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

    cmd = msg.split()
    if cmd[0] in ["h", "http"]:
        try:
            res = status[int(cmd[1])]
        except KeyError:
            res = "The specified status is undefined"
    else:
        res = msg

    return res


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(dispatch_response(event.message.text)))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
