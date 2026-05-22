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


@app.route('/', methods=['GET', 'POST'])
def home():

    # Default values
    prediction_text = ""
    area = ""
    bhk = ""
    bathroom = ""
    selected_locality = ""

    if request.method == 'POST':

        # Get form data
        area = request.form['area']
        bhk = request.form['bhk']
        bathroom = request.form['bathroom']
        selected_locality = request.form['locality']

        # Create dataframe
        input_data = pd.DataFrame(columns=columns)

        input_data.loc[0] = 0

        # Fill features
        input_data['area'] = float(area)
        input_data['bedroom_num'] = int(bhk)
        input_data['bathroom_num'] = int(bathroom)

        # Locality encoding
        locality_column = 'locality_' + selected_locality

        if locality_column in input_data.columns:
            input_data[locality_column] = 1

        # Prediction
        prediction = model.predict(input_data)[0]

        # Convert to crore
        prediction_cr = round(prediction / 10000000, 2)

        prediction_text = f"Estimated Price: ₹ {prediction_cr} Cr"

    return render_template(
        'index.html',
        prediction_text=prediction_text,
        localities=localities,
        area=area,
        bhk=bhk,
        bathroom=bathroom,
        selected_locality=selected_locality
    )


if __name__ == "__main__":
    app.run(debug=True)