import warnings
warnings.filterwarnings('ignore')


from flask import Flask, request, jsonify
import joblib
import numpy as np

model = joblib.load('loan_approval_pipeline.pkl')

app = Flask(__name__)


# add home route
@app.route('/')
def home():
    return '''
    <h2>Welcome to the Loan Approval Prediction API</h2>
    <p>This is a simple API for predicting loan approvals.</p>
    '''

#prediction route
@app.route('/predict', methods=['POST'])


def predict():
    data = request.json

    features = np.array([
        data['no_of_dependents'],
        data['income_annum'],
        data['loan_amount'],
        data['loan_term'],
        data['cibil_score'],
        data['residential_assets_value'],
        data['commercial_assets_value'],
        data['luxury_assets_value'],
        data['education'],
        data['self_employed'],
        data['bank_asset_value'],

    ])


    #prediction
    prediction = model.predict(features)
    probability = model.predict_proba(features)
    result = "Loan approved"

    if prediction[0] == 0:
        result = "Loan rejected"

    #confidence score
    confidence_score = np.max(probability)*100


    return jsonify({
        'prediction': result,
        'confidence': str(confidence_score)
    })

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )