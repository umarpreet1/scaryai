from flask import Flask
from flask import render_template
from flask import request
import requests
import random

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():  # put application's code here
    prompt_options = ["I was walking home alone and","Last summer, i went camping with my boyfriend and","Once driving on a country road at night I saw"]
    prompt = random.choice(prompt_options)
    return render_template("index.html",prompt=prompt)


def get_inference(prompt,max_new_tokens):
    payload = {"prompt":prompt,"max_new_tokens":max_new_tokens}
    result = requests.post('http://147.182.156.31:5000/generate',params=payload)
    result = result.json()
    return result['generated_sequence']

@app.route('/generate',methods=['GET','POST'])
def generate():
    prompt = request.form.get("prompt")
    print(prompt)
    prompt = get_inference(prompt,20)
    print(prompt)
    return render_template("index.html",prompt=prompt)



if __name__ == '__main__':
    app.run()
