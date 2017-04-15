import json

from flask import Flask, request, render_template
import requests

import config


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', sitekey=config.recaptcha_sitekey)

@app.route('/post', methods=['POST'])
def recaptcha_verify():
    captcha_res = request.form.get('g-recaptcha-response', '')
    if len(captcha_res) == 0:
        return 'failed...'
    
    param = {
        'secret': config.recaptcha_secretkey,
        'response': captcha_res,
        'remoteip': request.remote_addr,
    }
    res = requests.post(config.recaptcha_verify_url, params=param)
    result = json.loads(res.text)
    return 'success verify!' if result['success'] else 'failed verify'

if  __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
