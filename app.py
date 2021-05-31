from flask import Flask, render_template, request, redirect, jsonify
import numpy as np
import xgboost
import pickle
from flask_cors import CORS

with open('ml_model.pkl', 'rb') as file:
    classifier = pickle.load(file)

app = Flask(__name__)
CORS(app)

@app.route('/predict-diabetes', methods=['GET', 'POST'])
def api_pred():
    inputs = request.json
    data_array = []
    result = dict()

    try:
        for data in inputs:
            data_array.append(float(inputs[data]["value"]))

        if len(data_array) < 8:
            result = {item: inputs[data]["value"]for item in inputs}

            result["success"] = False
            result["prediction_result"] = None
            return jsonify(result)

    except:
        result["success"] = False
        result["prediction_result"] = None
        result["message"] = "Invalid Input"

        return jsonify(result)

    data = np.array([data_array])
    prediction = classifier.predict(data)

    result = {
        'num_preg': inputs["num_preg"]["value"],
        'glucose_conc': inputs["glucose_conc"]["value"],
        'diastolic_bp': inputs["diastolic_bp"]["value"],
        'thickness': inputs["thickness"]["value"],
        'insulin': inputs["insulin"]["value"],
        'bmi': inputs["bmi"]["value"],
        'dpf': inputs["dpf"]["value"],
        'age': inputs["age"]["value"],
        'prediction_result': bool(prediction[0])
    }
    
    return jsonify(result)

@app.route('/<int:num_preg>/<int:glucose_conc>/<int:diastolic_bp>/<int:thickness>/<int:insulin>/<float:bmi>/<float:dpf>/<int:age>')
def api_predu(num_preg,glucose_conc,diastolic_bp,thickness,insulin,bmi,dpf,age):
    data=np.array([[int(num_preg),int(glucose_conc),int(diastolic_bp),int(thickness),int(insulin),float(bmi),float(dpf),int(age)]])
    prediction=classifier.predict(data)

    result={
            'num_preg':num_preg,
            'glucose_conc':glucose_conc,
            'diastolic_bp':diastolic_bp,
            'thickness':thickness,
            'insulin':insulin,
            'bmi':bmi,
            'dpf':dpf,
            'age':age,
            'prediction_result':bool(prediction[0])
        }

    return jsonify(result)
@app.route('/<string:name>/<int:data1>/<int:data2>/<int:data3>/<int:data4>/<int:data5>')
def api_ret(name,data1,data2,data3,data4,data5):
    
    result={
            'name':name,
            'data':[data1,data2,data3,data4,data5],

        }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
