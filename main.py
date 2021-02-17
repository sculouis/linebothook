from flask import Flask, request, abort,render_template
import os
import configparser

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')
token = config.get('line-bot','channel_access_token')
secret = config.get('line-bot','channel_secret')
print(token)
print(secret)
line_bot_api = LineBotApi(token)
handler = WebhookHandler(secret)

@app.route("/")
def hello_world():
    return render_template("index.html") 

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_message = "您傳送的訊息:" + event.message.text
    print(reply_message)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)