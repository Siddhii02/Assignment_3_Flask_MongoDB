from flask import Flask , render_template, request
import requests

app=Flask(__name__)
BACKEND_URL='http://127.0.0.1:9000'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    form_data=dict(request.form)
    try:
        response=requests.post(BACKEND_URL+'/submit', json=form_data)
        return render_template('success.html')
    except requests.exceptions.RequestException as e:
        return render_template('index.html',error=str(e))

if __name__ =='__main__':
    app.run(port=5000,debug=True)
