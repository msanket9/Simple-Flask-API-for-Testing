from flask import Flask, render_template, request, redirect, jsonify
import numpy as np
import xgboost
from flask_cors import CORS



app = Flask(__name__)
CORS(app)


@app.route('/<string:name>/<int:data1>/<int:data2>/<int:data3>/<int:data4>/<int:data5>')
def api(name,data1,data2,data3,data4,data5):
    
    result={
            'name':name,
            'data':[data1,data2,data3,data4,data5],

        }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)