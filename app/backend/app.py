from flask import Flask, render_template, Response, request
from dotenv import load_dotenv
from utils.util_functions import gen_frames
from utils.config import config

load_dotenv()

app = Flask(__name__)


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/toggle_yolo', methods=['POST'])
def toggle_yolo():
    config.yolo_enabled = not config.yolo_enabled
    return {'status': 'success', 'yolo_enabled': config.yolo_enabled}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            new_interval = int(request.form.get('interval'))
            if new_interval >= config.min_interval:
                config.min_interval = new_interval
        except ValueError:
            pass
    return render_template('index.html', min_interval=config.min_interval)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
