#!/usr/bin/python3.10

from flask import Flask, jsonify, request
import pickle

with open('model2.bin', 'rb') as f_in: # very important to use 'rb' here, it means read-binary 
    model = pickle.load(f_in)

with open('dv.bin', 'rb') as f_n: # very important to use 'rb' here, it means read-binary 
    dv = pickle.load(f_n)

app = Flask('ping') 



def predict_single(customer, dv, model):
  X = dv.transform([customer])  ## apply the one-hot encoding feature to the customer data 
  y_pred = model.predict_proba(X)[:, 1]
  return y_pred[0]


@app.route('/predict', methods=['POST'])  ## in order to send the customer information we need to post its data.
def predict():
    customer = request.get_json()  
    prediction = predict_single(customer, dv, model)
    churn = prediction >= 0.5

    result = {
        'churn_probability': float(prediction), 
        'churn': bool(churn),  
    }

    return jsonify(result)

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=9696) 