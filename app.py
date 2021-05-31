#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@create Time:2021-05-19

@author:LHQ
"""
from flask import Flask, request, jsonify

from model import init_model, predict, update_model


app = Flask(__name__)
    

@app.before_first_request
def load_model():  
    init_model()


@app.route("/predict")
def api_predict():
    x = request.args.get("x", default=0, type=float)
    result = predict(x)
    return jsonify(args=x, result=result)
    

@app.route("/update")
def api_update():
    info = update_model()
    return jsonify({"status": "success", "updating model":info})
