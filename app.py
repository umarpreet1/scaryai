from flask import Flask
from flask import render_template
from flask import request
import requests
import random
import json

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():  # put application's code here
    prompt_options = ["I was walking home alone and","Last summer, i went camping with my boyfriend and","Once driving on a country road at night I saw"]
    prompt = random.choice(prompt_options)
    return render_template("index.html",prompt=prompt)


def get_inference(prompt,max_new_tokens):
    #payload = {"prompt":prompt,"max_new_tokens":max_new_tokens}
    #result = requests.post('http://147.182.156.31:5000/generate',params=payload)
    #result = result.json()
    apiKey = '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'
    model = 'ada:ft-personal-2023-01-31-16-19-18'
    prompt = prompt

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {apiKey}'
    }

    data = {
    'model': model,
    'prompt': prompt,
    'max_tokens': 30,
    'temperature': 0.8,
    'top_p': 0.95,
    }

    response = requests.post('https://api.openai.com/v1/completions', headers=headers, data=json.dumps(data))
    json_response = response.json()
    result = json_response['choices'][0]['text']
    prompt = prompt + result
    return prompt

@app.route('/generate',methods=['GET','POST'])
def generate():
    prompt = request.form.get("prompt")
    print(prompt)
    prompt = get_inference(prompt,20)
    print(prompt)
    return render_template("index.html",prompt=prompt)



if __name__ == '__main__':
    app.run()
