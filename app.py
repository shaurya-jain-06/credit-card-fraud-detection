import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from keras.models import load_model
model=load_model("cc_fraud.h5")

from pymongo import MongoClient
client=MongoClient("localhost",27017)
db=client.neuraldb

app = Flask(__name__)
# prediction function 
def ValuePredictor(to_predict_list): 
     
     
    result = model.predict([to_predict_list]) 
    return result[0]     
    
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict() 
        to_predict_list = list(to_predict_list.values())
        print(to_predict_list)
        
        
        to_predict_list = list(map(float, to_predict_list))
        cc_num=to_predict_list.pop(-1)
        result = ValuePredictor(to_predict_list)
        
        res=result[0]*100
        
    if result[0]>0.5:
        prediction ='Given transaction has a ' +str(res)+'% chance of being fradulent'
        db.cc_fraud.insert_one({"credit card number":cc_num,"amount":to_predict_list[0],"age":to_predict_list[3],"city code":to_predict_list[1]})
    else:
        db.cc_history.insert_one({"credit card number":cc_num,"amount":to_predict_list[0],"age":to_predict_list[3],"city code":to_predict_list[1]})
        prediction ='Given transaction is NOT fradulent'            
    return render_template("result.html", prediction = prediction) 
    
            
if __name__ == "__main__":
    app.run(debug=True)
