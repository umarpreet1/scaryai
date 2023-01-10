from flask import Flask
from flask import render_template
from flask import request
import random
import onnxruntime as ort
from  transformers import AutoConfig
from optimum.onnxruntime import ORTModelForCausalLM
from transformers import AutoTokenizer

ort_sess = ort.InferenceSession('../model/decoder_model_quantized.onnx',providers=['CPUExecutionProvider'])

config = AutoConfig.from_pretrained('../model')

model = ORTModelForCausalLM(ort_sess,model_save_dir="../model/",config=config)

tokenizer = AutoTokenizer.from_pretrained("gpt2-large")

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():  # put application's code here
    prompt_options = ["I was walking home alone and","Last summer, i went camping with my boyfriend and","Once driving on a country road at night I saw"]
    prompt = random.choice(prompt_options)
    return render_template("index.html",prompt=prompt)

@app.route('/generate',methods=['GET','POST'])
def generate():
    prompt = request.form.get("prompt")
    print(prompt)
    prompt = get_inference(prompt,20)
    print(prompt)
    return render_template("index.html",prompt=prompt)


def get_inference(prompt, new_tokens):

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    input_ids = input_ids.to(model.device)

    outputs = model.generate(input_ids, do_sample=True, max_new_tokens=new_tokens)

    result = prompt = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

    return result


if __name__ == '__main__':
    app.run()
