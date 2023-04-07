from flask import Flask, request, render_template, Response
import cv2
import numpy as np
import qrcode
import pyzbar.pyzbar as pyzbar

app = Flask(__name__)
camera = cv2.VideoCapture(0)

@app.route('/')
def home():
    return render_template('home.html')

def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            decoded = pyzbar.decode(frame)
            if decoded:
                yield f"data: {decoded[0].data.decode('utf-8')}\n\n"
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\n'
                   b'Content-Type: image/jpeg\n\n' + frame + b'\n')  # concat frame one by one and show result

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/scan', methods=['POST'])
def scan():
    file = request.files['image']
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    decoded = pyzbar.decode(img)
    return decoded[0].data.decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)
