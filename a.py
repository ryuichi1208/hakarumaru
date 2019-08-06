
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, AudioMessage
)
import os

YOUR_CHANNEL_SECRET = "610989f0eb3dd983010087a2bbc4b7ea"
YOUR_CHANNEL_ACCESS_TOKEN = "YNvQUWGAzSTIIMzyPgkBIaktnNZQgR4YkvUBZGFQIjWcSAFu8acgj94ePqeJGCN1isSyyc0QKCbYEx2gN50TLf+ordWojC+XT4gZyyXSWVxoObh9WSiioLbpgg6JWyxyLYgJXXQ8rEXacb3hpOXW0AdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

def return_ok():

    return 'OK'

return_ok()
