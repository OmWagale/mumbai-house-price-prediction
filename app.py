from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model
model = pickle.load(open('model/house_price_model.pkl', 'rb'))

# Load training columns
columns = pickle.load(open('model/columns.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    # User Inputs
    area = float(request.form['area'])
    bhk = int(request.form['bhk'])
    bathroom = int(request.form['bathroom'])
    locality = request.form['locality']

    # Create empty dataframe
    input_data = pd.DataFrame(columns=columns)

    # Add one row
    input_data.loc[0] = 0

    # Fill main features
    input_data['area'] = area
    input_data['bedroom_num'] = bhk
    input_data['bathroom_num'] = bathroom

    # Fill locality column
    locality_column = 'locality_' + locality

    if locality_column in input_data.columns:
        input_data[locality_column] = 1

    # Prediction
    prediction = model.predict(input_data)[0]

    # Convert to lakhs
    prediction_lakh = round(prediction / 100000, 2)

    return render_template(
        'index.html',
        prediction_text=f"Estimated Price: ₹ {prediction_lakh} Lakhs"
    )


if __name__ == "__main__":
    app.run(debug=True)