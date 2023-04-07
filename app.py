from flask import Flask, render_template, request, redirect, url_for
from pyzbar.pyzbar import decode
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    file = request.files['image']
    img = Image.open(file.stream)
    result = decode(img)
    if result:
        return redirect(url_for('result', code=result[0][0]))
    else:
        return redirect(url_for('index'))

@app.route('/result/<code>')
def result(code):
    return render_template('result.html', code=code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
