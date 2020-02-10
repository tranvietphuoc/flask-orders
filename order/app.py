from flask import Flask, render_template, redirect, request, flash, url_for
import requests
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['TEMPLATES_AUTO_RELOAD'] = True
url = 'https://console.ghn.vn/api/v1/apiv3/OrderInfo'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/info', methods=['GET', 'POST'])
def info():

    if request.method == 'POST':
        # token = str(request.args.get('token'))  # login at https://api.ghn.vn to get token access
        token = request.values.get('token')  # use request.values to get value from form
        # orders = str(request.args.get('ordercode')).split(',')  # list of ordercodes
        orders = request.values.get('ordercode').split(',')  # use request.values to get value from form
        error = None
        results = []
        if not token:
            error = "Token string is required"
        elif not orders:
            error = "OrderCode is required"
        else:
            for order in orders:
                data = dict()
                data.update({'token': token, 'OrderCode': order})
                try:
                    response = requests.post(
                        url, data=json.dumps(data), headers=headers)
                    # if response is successfully, there no Exception will be raised
                    response.raise_for_status()
                except requests.exceptions.HTTPError as http_err:
                    message = f'HTTP error occured: {http_err}'
                    flash(message)
                    return render_template('http-error.html', message=message)
                except Exception as err:
                    message = f'Other error occured: {err}'
                    flash(message)
                    return render_template('http-error.html', message=message)
                else:
                    # print('Success!')
                    results.append(json.loads(response.text)['data'])
        if error is not None:
            flash(error)
        
    return render_template('info.html', results=results)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    port = int(os.environ.get('PORT', 5000))
    a
