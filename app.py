from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model
model = pickle.load(open('model/house_price_model.pkl', 'rb'))

# Load columns
columns = pickle.load(open('model/columns.pkl', 'rb'))

# Extract localities
localities = []

for col in columns:
    if col.startswith('locality_'):
        localities.append(col.replace('locality_', ''))

localities.sort()


@app.route('/')
def home():

    return render_template(
        'index.html',
        localities=localities
    )


@app.route('/predict', methods=['POST'])
def predict():

    # Get form data
    area = request.form['area']
    bhk = request.form['bhk']
    bathroom = request.form['bathroom']
    locality = request.form['locality']

    # Create dataframe
    input_data = pd.DataFrame(columns=columns)

    input_data.loc[0] = 0

    # Fill features
    input_data['area'] = float(area)
    input_data['bedroom_num'] = int(bhk)
    input_data['bathroom_num'] = int(bathroom)

    # Handle locality
    locality_column = 'locality_' + locality

    if locality_column in input_data.columns:
        input_data[locality_column] = 1

    # Predict
    prediction = model.predict(input_data)[0]

    # Convert to crore
    prediction_cr = round(prediction / 10000000, 2)

    return render_template(
        'index.html',
        prediction_text=f"Estimated Price: ₹ {prediction_cr} Cr",
        localities=localities,
        area=area,
        bhk=bhk,
        bathroom=bathroom,
        selected_locality=locality
    )


if __name__ == "__main__":
    app.run(debug=True)