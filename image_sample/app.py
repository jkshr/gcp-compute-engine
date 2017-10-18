# coding:utf-8

# ---app.py---

from flask import Flask, render_template, Response,request,redirect,url_for
import datetime
#from PIL import Image
import qrcode as qr
import base64
from io import BytesIO

# flask incetance
app = Flask(__name__)

# index page, input code
@app.route('/')
def index():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    return render_template('index.html',time=timeString)


@app.route('/input_code', methods=['POST'])
def input_code():
    code_input = request.form['code']
    qr_b64data = qrmaker(str(code_input))
    ts = datetime.datetime.now()
    qr_name = "qrcode_image_{}".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
    return render_template("output_code.html",
        data=code_input,
        qr_b64data=qr_b64data,
        qr_name=qr_name
    )

# retry and quit
@app.route('/event', methods=['POST'] )
def event():
    if request.method == 'POST':
        if request.form['submit'] == 'Retry':
           return redirect(url_for('index'))
        elif request.form['submit'] == 'Quit':
            return Response('Please close the web browser')
        else:
            pass # unknown
    elif request.method == 'GET':
        return redirect(url_for('index'))

# QRmakerという名前はpythonの命名規則に反するように思われるのですべて小文字にしました。
def qrmaker(code):
    qr_img = qr.make(str(code))

    # 画像書き込み用バッファを確保して画像データをそこに書き込む
    buf = BytesIO()
    qr_img.save(buf,format="png")

    # バイナリデータをbase64でエンコードし、それをさらにutf-8でデコードしておく
    qr_b64str = base64.b64encode(buf.getvalue()).decode("utf-8")

    # image要素のsrc属性に埋め込めこむために、適切に付帯情報を付与する
    qr_b64data = "data:image/png;base64,{}".format(qr_b64str)

    return qr_b64data


# メニュー画面作成
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
