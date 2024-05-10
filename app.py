from flask import Flask, request, render_template, jsonify
from boltiotai import openai
import pandas as pd

app = Flask(__name__)

openai.api_key = 'UVO3uaZybJTl1ZjnKyA1yjVrNUpyfCvg-Rrn2UR-wYg'

name = None

def get_plan(age,goal,desired_weight,present_weight,height,lifestyle,injuries,style,time,sex):
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "You are a helpful assistant and AI health assistant having all knowledge related to health and fitness"
        }, {
            "role": "user",
            "content": f"Create a {goal} workout plan for me, my goal is {goal} in a healthy manner, weight is {present_weight} and height is {height} and my desired weight is {desired_weight} create plan accordingly. My injury status is {injuries}. Please also tell me my BMI and maintenance calories my age is {age} and here are my other details gender {sex}, my lifestyle is {lifestyle}, I would prefer a {style} type of workout and I can devote {time} in a day."
        }]
    )

    # Extracting the content from the response
    content = response['choices'][0]['message']['content']
    
    return content

def modify(prediction, modifications):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "You are a helpful assistant and AI health assistant having all knowledge related to health and fitness"
        }, {
            "role": "user",
            "content": f"Sorry but I have a problem with {prediction}. My issue is/are {modifications}. Please revise it accordingly"
        }]
    )

    content = response['choices'][0]['message']['content']
    return content

def foodPlan(diet, allergies):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "You are a helpful assistant and AI diet assistant having all knowledge related to health and nutrition."
        }, {
            "role": "user",
            "content": f"{diet}, I am allergic to {allergies}"
        }]
    )

    content = response['choices'][0]['message']['content']
    return content

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/work')
def work():
    return render_template('workout.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json  # Parse JSON data
    components = data['data']  # Access 'data' field
    actual_data = list(components.values())
    age = actual_data[0]
    goal = actual_data[1]
    desired_weight = actual_data[2]
    present_weight = actual_data[3]
    height = actual_data[4]
    lifestyle = actual_data[5]
    injuries = actual_data[6]
    style = actual_data[7]
    time = actual_data[8]
    sex = actual_data[9]
    plan = get_plan(age,goal,desired_weight,present_weight,height,lifestyle,injuries,style,time,sex)
    print(plan)
    length = len(plan)
    return jsonify({'success': True, 'plan': plan})

@app.route("/change",methods=['POST'])
def change():
    data = request.json
    data = data['data']
    actual_data =list(data.values())
    modifications = actual_data[0]
    prediction = actual_data[1]
    revisedPlan = modify(prediction,modifications)
    print(revisedPlan)
    return jsonify({'success':True,'revisedPlan':revisedPlan})


@app.route('/food')
def food():
    return render_template('food.html')


@app.route('/getFood',methods=['POST'])
def getFood():
    data = request.json
    data = data['data']
    actual_data =list(data.values())
    print(actual_data)
    diet = actual_data[0]
    allergies = actual_data[1]
    plan = foodPlan(diet, allergies)
    print(plan)
    return jsonify({'success':True,'food':plan})



if __name__ == "__main__":
    app.run(port=8000,debug=True)
