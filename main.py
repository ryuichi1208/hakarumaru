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

YOUR_CHANNEL_SECRET = "7d8a1d28358c5363864ccd0fe709f9e7"
YOUR_CHANNEL_ACCESS_TOKEN = "MEspC++mz0TZAMQhNsh4Xvz0R2XOZCKTvXMDZ0eH3igQ1ozbh08OgSPvIKJhchzfisSyyc0QKCbYEx2gN50TLf+ordWojC+XT4gZyyXSWVz9fJK/6PEYUtoYhAQHRX3MCAhAwxGLWHdTCpHlKTm+uwdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def return_ok():
    return 'OK'

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    print(body)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
