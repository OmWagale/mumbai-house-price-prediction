from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load trained model
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
    area = float(request.form['area'])
    bhk = int(request.form['bhk'])
    bathroom = int(request.form['bathroom'])
    locality = request.form['locality']

    # Create dataframe with all columns
    input_data = pd.DataFrame(columns=columns)

    # Fill all values with 0
    input_data.loc[0] = 0

    # Add user inputs
    input_data['area'] = area
    input_data['bedroom_num'] = bhk
    input_data['bathroom_num'] = bathroom

    # Handle locality
    locality_column = 'locality_' + locality

    if locality_column in input_data.columns:
        input_data[locality_column] = 1

    # Predict price
    prediction = model.predict(input_data)[0]

    # Convert to Crores
    prediction_cr = round(prediction / 10000000, 2)

    return render_template(
        'index.html',
        prediction_text=f"Estimated Price: ₹ {prediction_cr} Cr",
        localities=localities
    )


if __name__ == "__main__":
    app.run(debug=True)